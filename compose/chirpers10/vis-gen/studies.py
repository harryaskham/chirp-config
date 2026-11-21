#!/usr/bin/env python3
"""Common Time's film: the studies (looks), as functions of the tracks they are given.

The film is a set of MOTION STUDIES: every scene is one way a camera can hold time in a still
picture (a plate flashed by the notes, a slit the film runs past, a sheet of panels, a lamp left
to draw its path), pointed at things that count: wheels, walkers, a smith. Nothing here is
written for one song: a study takes track names, and reads from each track its notes
(`track.T.hit`), its level, and its CELL (`track.T.cell`, `track.T.turn`: the length of its
repeating riff in sixteenths and the turns of a wheel that goes round once per cell, both found
by the engine from the notes). So the same studies fit any version of any song.

Silver on black, with one spot colour a song.
"""

import math

INK = "#f2efe6"      # the silver
DIM = "#8f8c84"
BLACK = "#000000"
# The camera every plate shares: far off and long, so the picture is flat like a lab plate.
# (+x is to the right with the camera on the -z side.)
CAM = {"x": 0, "y": 0, "z": -9, "look_at": [0, 0, 0], "zoom": 2.2}
# A layer's own zoom is 1.6, so a world unit at z = 0 is K picture units (the frame is 2 tall):
# the frame shows about 5.1 units up and down and 9.1 across.
K = 1.6 * CAM["zoom"] / 9
HALF_H, HALF_W = 1 / K, (16 / 9) / K


def lit(color=INK, emit=1.0):
    """A body that is its own light (white on the black plate)."""
    return {"color": color, "emit": emit, "light": 0, "ambient": 1, "rim": 0}


def backdrop(level=0.16, z=1.0):
    """The plate's ground: black, ruled in fine white threads every half unit and a heavier one
    every two (Muybridge's wall), so there is always a measure behind what moves. Threads are
    thin boxes (a few dozen, cheap to draw), not a painted wall."""
    out = []
    for n, gap, lev, wide in ((25, 0.5, 0.55 * level, 0.0045), (7, 2.0, level, 0.007)):
        mid = (n - 1) / 2
        out.append({"type": "mesh", "shape": "box", "round": 0.02, "detail": 2, "count": n, "x": f"(inst.i - {mid:g})*{gap}", "y": 0, "z": z, "scale": 1,
                    "sx": wide, "sy": 3.6, "sz": 0.002, **lit(INK, lev)})
        out.append({"type": "mesh", "shape": "box", "round": 0.02, "detail": 2, "count": n, "x": 0, "y": f"(inst.i - {mid:g})*{gap}", "z": z, "scale": 1,
                    "sx": 6.4, "sy": wide, "sz": 0.002, **lit(INK, lev)})
    return out


def border(spot, when="env.all"):
    """The plate's border, in the spot colour, lit by `when`: every study lights it where all
    its cycles meet, so the one sign means the same thing all through the film."""
    w, h = HALF_W - 0.22, HALF_H - 0.18
    out = []
    for x, y, sx, sy in ((0, h, w, 0.008), (0, -h, w, 0.008), (-w, 0, 0.008, h), (w, 0, 0.008, h)):
        out.append({"type": "mesh", "shape": "box", "round": 0.02, "detail": 2, "x": round(x, 3), "y": round(y, 3), "z": -0.2, "scale": 1,
                    "sx": round(sx, 3), "sy": round(sy, 3), "sz": 0.004, "opacity": when, **lit(spot, 1.5)})
    return out


def finish(spot):
    """A plate's own finish: halation round the bright parts. (The print itself, its grain and
    dark corners, and whether it is a negative, belong to the song's master: see `master`.)"""
    # The low end overexposes: the heavier the music, the more the light spreads in the
    # emulsion. A quiet passage is drawn in hard thin lines; a heavy one burns.
    return [{"type": "bloom", "threshold": 0.5, "amount": "0.2 + 1.0*audio.low", "radius": "0.012 + 0.016*audio.low"}]


def master(number, title, white=False, figures=(), bars=0, window=None):
    """What lies over every scene of a song: the plate's name for its first bars, a legend in
    the corner (the plate, and which figure of it this scene is: `figures` is each scene's
    (first bar, bars)), and the print. `white`: the song is printed as a negative, black
    figures on a pale ruled wall (the spot colour turns to its complement, an ink).
    `window` (first bar, last bar): an excerpt, which opens on the name at its own first bar
    and comes up from black and goes back to it by itself."""
    bar = f"(time.bar - {window[0]})" if window else "time.bar"
    label = [
        # The plate is all but blank while its name is up, then comes up under it as a print
        # does in the tray.
        {"type": "shape", "sides": 4, "radius": 4, "width": 0, "fill": 1, "color": "#161616", "blend": "multiply", "opacity": f"1 - smooth(2.4, 4.6, {bar})"},
        {"type": "text", "text": f"PLATE {number:02d}", "size": 0.05, "x": 0, "y": 0.2, "align": "center", "color": DIM, "width": 0.11, "skew": 0,
         "opacity": f"smooth(0.1, 0.6, {bar})*(1 - smooth(3.2, 4.2, {bar}))"},
        {"type": "text", "text": title.upper(), "size": 0.17, "x": 0, "y": -0.07, "align": "center", "color": INK, "width": 0.12, "skew": 0,
         "opacity": f"1 - smooth(3.2, 4.2, {bar})", "reveal": f"smooth(0.3, 1.6, {bar})"},
    ]
    if figures:
        label.append({"type": "captions", "size": 0.034, "x": -1.7, "y": -0.955, "align": "left", "color": DIM, "width": 0.1, "skew": 0, "glow": 0, "typing": 0, "fade": 0.4,
                      "opacity": 0.9, "lines": [[f"{a}bar" if a else 0, f"{b}bar", f"PL. {number:02d}   FIG. {k + 1}"] for k, (a, b) in enumerate(figures)]})
    if white and bars:
        # A negative comes up from black and goes back to it: a programme's own fade is taken
        # before the print is turned over, and would leave a blank white page at each end.
        label.append({"type": "shape", "sides": 4, "radius": 4, "width": 0, "fill": 1, "color": "#ffffff",
                      "opacity": f"max(1 - smooth(0, 1, time.bar), smooth({1 - 2 / bars:.5f}, 1, time.progress))"})
    filters = ([{"type": "invert"}, {"type": "color", "brightness": -0.05, "contrast": 0.94}] if white else []) + [
        {"type": "grain", "amount": 0.05},
        {"type": "vignette", "amount": 0.3 if white else 0.55},
    ]
    if window:
        # Over the print, so a negative's excerpt goes to black too.
        filters.append({"type": "color", "brightness": f"0 - 2*max(1 - smooth(0, 0.5, {bar}), smooth({window[1] - window[0] - 1}, {window[1] - window[0]}, {bar}))"})
    return {"layers": label, "filters": filters}


def clock(track, celled=True, per_bar=1.0):
    """What turns a track's body. A track with a cell turns once per cell (`track.T.turn`: it
    stands still where the track rests). One without (a tune, a voice, plain common time) is
    turned by the bar instead, `per_bar` times a bar."""
    return f"track.{track}.turn" if celled else f"time.bar*{per_bar:g}"


def teeth(track, celled=True):
    """How many sixteenths its wheel has: its cell, or a bar of common time."""
    return f"track.{track}.cell" if celled else "16"


# ───────────────────────── the wheel (a riff draws its own necklace) ─────────────────────────

def wheel_look(track, color=INK, fade="24/time.bpm", live=0.3, celled=True, each=0.1):
    """One wheel's pointer for one track, on its own plate. It goes round once per cell; the
    plate is flashed by the track's notes, so the pointer prints where in the cell each note
    falls: the riff draws its own necklace, and holds it still for as long as it repeats.
    params: cx, cy (where), r (radius)."""
    T = clock(track, celled)
    has = f"step(0.5, {teeth(track, celled)})"
    return {
        "params": {"cx": 0, "cy": 0, "r": 1},
        "background": BLACK,
        "camera": CAM,
        "layers": [
            # The pointer: from the hub to the rim, turning with the riff.
            {"type": "mesh", "shape": "box", "round": 0.02, "detail": 2,
             "x": f"param.cx + 0.5*param.r*sin({T})", "y": f"param.cy + 0.5*param.r*cos({T})", "z": 0, "rz": f"0 - {T}",
             "scale": "param.r*0.5", "sx": 0.03, "sy": 1, "sz": 0.03, "opacity": has, **lit(color, 1.0)},
            # Its tip: a bead on the rim.
            {"type": "mesh", "shape": "sphere", "detail": 12, "x": f"param.cx + param.r*sin({T})", "y": f"param.cy + param.r*cos({T})", "z": 0,
             "scale": "0.07 + 0.03*track.%s.hit" % track, "opacity": has, **lit(color, 1.6)},
        ],
        # Each note dims the older prints a little, so the plate keeps the riff's last twenty
        # notes or so however fast they come, and holds them while the riff rests.
        "filters": [{"type": "expose", "on": f"track.{track}", "fade": fade, "each": each, "live": live}],
    }


def wheel_rim(track, x, y, r, celled=True, color=DIM, glow="0"):
    """The wheel itself, standing in the scene (not on the plate): a hoop, a hub, and a tooth
    for every sixteenth of the cell, so the wheel has as many teeth as the riff is long.
    `r` may be an expression (a wheel that grows with its riff); `glow` lights the hoop."""
    C = teeth(track, celled)
    N = f"max({C}, 1)"
    # A wheel whose riff rests stands faint (an empty hoop should not hold the plate).
    awake = f"(0.3 + 0.7*clamp(track.{track}.level*8, 0, 1))"
    return [
        {"type": "shape", "sides": 0, "radius": f"({r})*{K:.4f}", "width": f"0.007 + 0.006*({glow})", "x": round(x * K, 4), "y": round(y * K, 4), "color": color,
         "opacity": f"(0.6 + 0.4*({glow}))*{awake}"},
        {"type": "mesh", "shape": "box", "round": 0.02, "detail": 2, "count": 48,
         "opacity": f"step(inst.i + 0.5, {C})*{awake}",
         "x": f"{x} + 1.07*({r})*sin(inst.i/{N})", "y": f"{y} + 1.07*({r})*cos(inst.i/{N})", "z": 0,
         "rz": f"0 - inst.i/{N}", "scale": 0.05, "sx": 0.18, "sy": "1 + step(inst.i, 0.5)*1.2", "sz": 0.18, **lit(color, 0.8)},
        {"type": "mesh", "shape": "sphere", "detail": 10, "x": x, "y": y, "z": 0, "scale": 0.05, **lit(color, 1.0)},
    ]


def together(tracks, plain=(), within=0.035):
    """An expression that is 1 while every one of these tracks is at the start of its cell at
    once (their wheels all at the top together), and 0 otherwise: where the cycles meet. Two
    riffs of five and seven sixteenths meet every thirty-five; add one of eleven and it is
    twenty-four bars. Nothing says when: it is read off the wheels."""
    parts = []
    for t in tracks:
        if t in plain:
            parts.append(f"step({1 - within*4:.3f}, cos(time.bar))")
        else:
            parts.append(f"step(0.5, track.{t}.cell)*step(cos({within}), cos(track.{t}.turn))")
    return "*".join(parts) if parts else "0"


def ruler(y=-2.15, color=DIM):
    """Common time, ruled along the foot of the plate: sixteen ticks a bar and a cursor that
    crosses them once a bar, whatever the wheels above are doing."""
    return [
        {"type": "mesh", "shape": "box", "round": 0.02, "detail": 2, "count": 17, "x": "-4 + inst.i*0.5", "y": y, "z": 0,
         "scale": 0.05, "sx": 0.12, "sy": "0.6 + 0.9*step(fract(inst.i/4), 0.1)", "sz": 0.12, **lit(color, 0.7)},
        {"type": "mesh", "shape": "sphere", "detail": 10, "x": "-4 + 8*time.barphase", "y": y + 0.16, "z": 0, "scale": 0.045, **lit(INK, 1.4)},
    ]


def wheels(tracks, spot, spot_track=None, plain=()):
    """Up to four wheels in a row, each a track's riff, each pointer on its own plate. A wheel
    is as big as its riff is long (so every pointer's tip goes at the same speed: the one
    pulse they share), and grows or shrinks when the riff changes. Where two neighbours come
    round together a thread lights between them; where all do, every hoop lights."""
    tracks = tracks[:4]
    n = len(tracks)
    rmax = {1: 1.8, 2: 1.75, 3: 1.38, 4: 1.04}[n]
    xs = {1: [0], 2: [-2.0, 2.0], 3: [-2.9, 0, 2.9], 4: [-3.3, -1.1, 1.1, 3.3]}[n]
    cy = 0.25
    vars_, env, layers, plates = {}, {}, [], []
    if n > 1:
        env["all"] = {"when": together(tracks, plain), "decay": 2.4}
    for i, (t, x) in enumerate(zip(tracks, xs)):
        col = spot if t == spot_track else INK
        C = teeth(t, t not in plain)
        vars_[f"r{i}"] = {"follow": f"{rmax}*(0.5 + 0.5*sqrt(clamp(({C} - 3)/13, 0, 1)))", "attack": "500ms", "release": "500ms"}
        layers += wheel_rim(t, x, cy, f"var.r{i}", celled=t not in plain, glow="env.all" if n > 1 else "0")
        plates.append({"type": "actor", "use": wheel_look(t, col, celled=t not in plain), "params": {"cx": x, "cy": cy, "r": f"var.r{i}"}, "key": 0, "mask": "none"})
        if i + 1 < n:
            # The thread between this wheel and the next, lit when they come round together.
            env[f"m{i}"] = {"when": together(tracks[i:i + 2], plain), "decay": 1.2}
            x2 = xs[i + 1]
            layers.append({"type": "mesh", "shape": "box", "round": 0.02, "detail": 2, "x": (x + x2) / 2, "y": cy, "z": 0.1, "scale": 1,
                           "sx": (x2 - x) / 2, "sy": 0.006, "sz": 0.006, "opacity": f"env.m{i}", **lit(spot, 1.4)})
    marks = border(spot) if n > 1 else []
    return {"vars": vars_, "env": env, "background": BLACK, "camera": CAM, "layers": backdrop() + layers + plates + ruler() + marks, "filters": finish(spot)}


# ───────────────────────── the disc (a phenakistoscope turned by a riff) ─────────────────────────

def disc_look(track, color, subject, slots, every=1, celled=True, r=1.4, tall_max=0.9):
    """One disc for one track, on its own plate: as many figures round it as the riff has
    sixteenths, each a little further through its stride than the one ahead. It turns once
    per cell, so every sixteenth carries each figure exactly into the next one's place; the
    plate is flashed by the track's notes, and so the ring stands still and the figures run on
    the spot, as on a phenakistoscope. Where the riff rests, no flash: they hang, and fade.
    `slots`: how many figures are made (the cell is read live, so the ring re-spaces itself if
    the riff changes); `every`: a figure every so many sixteenths (long riffs)."""
    rig, motion, tall, thick, strides, ry = SUBJECTS[subject]
    T = clock(track, celled)
    C = f"max({teeth(track, celled)}, 1)"
    # A figure is as long as its share of the rim allows, and no taller than `tall_max`.
    long_ = 1.5 if rig == "horse" else (0.9 if rig == "human" else 1.4)
    size = f"min({tall_max / tall:.3f}, {0.8 * 6.2832 * r / long_:.3f}*{every}/{C})"
    layers = []
    for i in range(slots):
        a = f"({T} + {i * every}/{C})"
        fig = subject_layer(subject, f"(0 - {i * every}/{C})", f"track.{track}.hit", color,
                            x=f"param.cx + {r}*sin({a})", y=f"param.cy + {r}*cos({a})", z=0, scale=size)
        fig["rz"] = f"0 - {a}"
        fig["opacity"] = f"step({i * every} + 0.5, {C})*step(0.5, {teeth(track, celled)})"
        fig["emit"] = 1.2
        if rig == "human":
            fig["thick"] = thick * 1.7      # small figures: sticks would not read
        layers.append(fig)
    return {
        "params": {"cx": 0, "cy": 0},
        "background": BLACK, "camera": CAM, "layers": layers,
        # Each flash lasts into the next, so the ring's light is steady and only the poses change.
        # Each note takes a fresh plate (no two poses on one), which then stands, dimming
        # slowly: a ring whose riff rests keeps its last picture.
        "filters": [{"type": "expose", "on": f"track.{track}", "each": 1, "fade": "5/time.bpm", "live": 0.2}],
    }


def discs(tracks, spot, spot_track=None, subject="horse", plain=(), cells=None):
    """Two or three discs side by side, each a track's riff, each with as many runners round it
    as the riff is long. They all turn at the one pulse; a five and a seven show the same
    stride at different lengths, and the hoops light where they come round together."""
    # Three rings of horses fit; people are narrow and need the room of two.
    tracks = tracks[:3 if SUBJECTS[subject][0] == "horse" else 2]
    n = len(tracks)
    cells = cells or {}
    r = {1: 1.7, 2: 1.5, 3: 1.12}[n]
    xs = {1: [0], 2: [-2.25, 2.25], 3: [-3.05, 0, 3.05]}[n]
    cy = 0.28
    env, layers, plates = {}, [], []
    if n > 1:
        env["all"] = {"when": together(tracks, plain), "decay": 2.4}
    for i, (t, x) in enumerate(zip(tracks, xs)):
        col = spot if t == spot_track else INK
        cell = int(cells.get(t) or (16 if t in plain else 8))
        every = 1 if cell <= 12 else (2 if cell <= 24 else 4)
        slots = max(1, min(12, -(-cell // every)))
        layers += wheel_rim(t, x, cy, 0.52 * r, celled=t not in plain, glow="env.all" if n > 1 else "0")
        tall = (0.72 if SUBJECTS[subject][0] == "horse" else 0.95) * r
        plates.append({"type": "actor", "use": disc_look(t, col, subject, slots, every, celled=t not in plain, r=r, tall_max=tall),
                       "params": {"cx": x, "cy": cy}, "key": 0, "mask": "none"})
    marks = border(spot) if n > 1 else []
    return {"env": env, "background": BLACK, "camera": CAM, "layers": backdrop() + layers + plates + ruler() + marks, "filters": finish(spot)}


# ───────────────────────── the train (riffs as gears in mesh) ─────────────────────────

def gears(tracks, spot, spot_track=None, plain=(), white=False):
    """Clockwork, in real light: a gear per riff with a tooth for every sixteenth of it, all in
    mesh. Every gear is let go one tooth a sixteenth (the one pulse they share), so a five turns
    faster than a seven and a seven than an eleven, and they mesh truly, each turning against
    its neighbour. One tooth of each carries a jewel in the spot colour; the jewels come to the
    top together only where the riffs do. Steel on a black plate, shadows from a lamp.
    The teeth are counted live, and the train is scaled to fill the plate whatever they are.
    A short riff's wheel is cut finer (two, three or four teeth to the sixteenth, the same for
    the whole train, so the ratios hold) and carries a stud on each tooth that is a sixteenth:
    a wheel of five is then ten teeth and five studs, not five paddles."""
    tracks = tracks[:3]
    n = len(tracks)
    if white:
        spot = negative(spot)
    vars_, env, layers = {}, {}, []
    C = [f"max({teeth(t, t not in plain)}, 3)" for t in tracks]
    # The pitch: how much rim a tooth takes, so that the train is 8 units across, its biggest
    # gear no more than 4.1 high, and no tooth absurdly large.
    biggest = C[0] if n == 1 else f"max({', '.join(C)})" if n == 2 else f"max({C[0]}, max({C[1]}, {C[2]}))"
    least = C[0] if n == 1 else f"min({', '.join(C)})" if n == 2 else f"min({C[0]}, min({C[1]}, {C[2]}))"
    # Teeth to the sixteenth: enough that the smallest wheel has a dozen or so, and no wheel
    # more than the forty-eight there are to hand out.
    vars_["k"] = {"follow": f"min(max(1, floor(14/{least})), max(1, floor(48/{biggest})))", "attack": "0ms", "release": "0ms"}
    vars_["p"] = {"follow": f"min(min(25.13/({' + '.join(C)}), 12.88/{biggest}), 0.8*var.k)", "attack": "400ms", "release": "400ms"}
    vars_["q"] = {"follow": "var.p/var.k", "attack": "0ms", "release": "0ms"}      # a tooth's share of the rim
    for i in range(n):
        vars_[f"g{i}"] = {"follow": f"var.p*{C[i]}/6.2832", "attack": "0ms", "release": "0ms"}
    # Where each stands: side by side, pitch circles touching, the train centred.
    total = " + ".join(f"var.g{i}" for i in range(n))
    for i in range(n):
        before = " + ".join(f"2*var.g{j}" for j in range(i))
        vars_[f"x{i}"] = {"follow": f"0 - ({total}) + {before + ' + ' if before else ''}var.g{i}", "attack": "0ms", "release": "0ms"}
    # How far each is turned, in teeth, so that every pair meshes (a tooth of one in a gap of
    # the next) whatever the two counts are.
    off = ["0"]
    for i in range(1, n):
        sign = "0.5" if i % 2 else "0 - 0.5"
        off.append(f"fract({sign} - ({off[i - 1]}) + var.k*(0.25*{C[i - 1]} + 0.75*{C[i]}) + 8)")
    if n > 1:
        env["all"] = {"when": together(tracks, plain), "decay": 2.4}
    steel = {"material": "pbr", "rough": 0.42, "metal": 0.7, "color": "#d8d8d4", "env_sky": "#e4e7ee", "env_ground": "#2c2c30", "light": 0.85, "ambient": 0.3, "rim": 0}
    cy = 0.12
    for i, t in enumerate(tracks):
        T = clock(t, t not in plain)
        # It goes by the tooth, as an escapement lets a wheel go: a tick every sixteenth, all
        # the gears together (that is what keeps them in mesh).
        vars_[f"s{i}"] = {"follow": f"{T}*{C[i]}", "attack": "0ms", "release": "0ms"}
        tick = f"(floor(var.s{i}) + smooth(0, 0.55, fract(var.s{i})))"
        turn = f"(({'' if i % 2 == 0 else '0 - '}var.k*{tick} + ({off[i]}))/({C[i]}*var.k))"
        r, x = f"var.g{i}", f"var.x{i}"
        # A riff that rests drops out of mesh: its gear sinks back toward the plate and dims.
        vars_[f"w{i}"] = {"follow": f"clamp(track.{t}.level*8, 0, 1)", "attack": "60ms", "release": "700ms"}
        awake = f"(0.4 + 0.6*var.w{i})"
        back = f"0.13*(1 - var.w{i})"
        # The rim (at the roots of the teeth; a torus of scale 1 has its ring at about 0.74),
        # three spokes and a hub.
        layers.append({"type": "mesh", "shape": "torus", "detail": 40, "x": x, "y": cy, "z": back, "rx": 0.25, "scale": f"({r} - 0.2*var.q)/0.82", "tube": 0.13, "sy": 0.6, **steel})
        for k in range(3):
            layers.append({"type": "mesh", "shape": "box", "round": 0.3, "detail": 3, "x": x, "y": cy, "z": back, "rz": f"0 - {turn} + {k / 6:.4f}", "scale": 1,
                           "sx": 0.045, "sy": f"{r} - 0.3*var.q", "sz": 0.03, **steel})
        layers.append({"type": "mesh", "shape": "sphere", "detail": 14, "x": x, "y": cy, "z": f"{back} - 0.02", "scale": 0.13, "sz": 0.6, **steel})
        # The teeth: as many as the riff has sixteenths, times the cut.
        Ck = f"({C[i]}*var.k)"
        layers.append({"type": "mesh", "shape": "box", "round": 0.35, "detail": 3, "count": 48, "opacity": f"step(inst.i + 0.5, {Ck})",
                       "x": f"{x} + {r}*sin({turn} + inst.i/{Ck})", "y": f"{cy} + {r}*cos({turn} + inst.i/{Ck})", "z": back,
                       "rz": f"0 - ({turn} + inst.i/{Ck})", "scale": "var.q", "sx": 0.2, "sy": 0.24, "sz": 0.07, **steel})
        # A stud on each tooth that is a sixteenth (where the wheel is cut finer than that).
        layers.append({"type": "mesh", "shape": "sphere", "detail": 8, "count": 48, "opacity": f"step(inst.i + 0.5, {C[i]})*step(1.5, var.k)",
                       "x": f"{x} + ({r} - 0.38*var.q)*sin({turn} + inst.i/{C[i]})", "y": f"{cy} + ({r} - 0.38*var.q)*cos({turn} + inst.i/{C[i]})", "z": f"{back} - 0.05",
                       "scale": "0.1*var.q + 0.014", **lit(INK, 1.3)})
        # The jewel on the first tooth: the riff's own colour, lit by its notes.
        col = spot if t == spot_track or n == 1 else INK
        layers.append({"type": "mesh", "shape": "sphere", "detail": 12, "x": f"{x} + {r}*sin({turn})", "y": f"{cy} + {r}*cos({turn})", "z": f"{back} - 0.07",
                       "scale": f"(0.17*var.q + 0.02)*{awake}", **lit(col, f"0.9 + 1.2*track.{t}.hit")})
    plate = [
        # The plate behind: black, taking the shadows.
        {"type": "mesh", "shape": "box", "round": 0.01, "detail": 2, "x": 0, "y": 0, "z": 0.24, "scale": 1, "sx": 7, "sy": 4, "sz": 0.05,
         "material": "pbr", "rough": 0.85, "metal": 0, "color": "#151516", "env_sky": "#6a6e76", "env_ground": "#060606", "light": 1, "ambient": 0.15, "rim": 0},
    ]
    marks = border(spot) if n > 1 else []
    return {
        "vars": vars_, "env": env, "background": BLACK,
        "camera": {"x": "1.1*sin(time.bar/24)", "y": "0.25 + 0.3*cos(time.bar/32)", "z": -9, "look_at": [0, 0, 0], "zoom": 2.2},
        "layers": [{"type": "light", "x": -2.5, "y": 3.5, "z": -7, "power": 1.6, "reach": 40, "color": "#fff6e8"}] + plate + backdrop(0.02, 0.18) + layers + ruler() + marks,
        "filters": [
            {"type": "shadowmap", "amount": 0.7, "soft": 3, "size": 1024, "sun": 0, "x": -2.5, "y": 3.5, "z": -7, "zoom": 2.2},
            {"type": "ao", "amount": 0.5, "radius": 0.04},
            {"type": "tonemap", "knee": 0.7},
            {"type": "aa"},
            # Steel does not burn as a plate does: only the jewels and the border glow.
            {"type": "bloom", "threshold": 0.92, "amount": "0.25 + 0.5*audio.low", "radius": 0.012},
        ] + ([{"type": "invert"}] if white else []),
    }


# ───────────────────────── the fence (a whole turn of a riff on one plate) ─────────────────────────

def fence_look(track, color, subject, celled=True, y=0.0, tall=1.8, span=7.6):
    """One lane on its own plate, under its own fence. The runner crosses the lane once per
    turn of the riff. The plate holds as many pictures as the riff has sixteenths, cut into
    strips and laid side by side in turn, and the fence over it has a gap every that many
    strips and slides a strip a sixteenth: so the gaps show the runner where it is now, whole,
    and between the pales, faintly, where it was at every other sixteenth of the turn. While
    the riff repeats, the plate stands still and only the fence moves."""
    rig, motion, rig_h, thick, strides, ry = SUBJECTS[subject]
    T = clock(track, celled)
    C = f"max({teeth(track, celled)}, 2)"
    long_ = 1.5 if rig == "horse" else 0.8
    # Big enough to be cut into many strips: with long riffs the runners overlap on the plate.
    size = f"min({tall / rig_h:.3f}, {0.9 * span / long_:.3f}/min({C}, 6))"
    fig = subject_layer(subject, T, f"track.{track}.hit", color,
                        x=f"{-span / 2:.2f} + {span}*(0.5/{C} + fract({T})*(1 - 1/{C}))", y=y, z=0, scale=size)
    fig["emit"] = 1.3
    if rig == "human":
        fig["thick"] = thick * 1.5
    return {
        "background": BLACK, "camera": CAM,
        "layers": [
            # The lane's ground: a faint light behind, so the fence itself is seen.
            {"type": "mesh", "shape": "box", "round": 0.01, "detail": 2, "x": 0, "y": y, "z": 0.3, "scale": 1, "sx": span / 2 + 0.5, "sy": tall * 0.62, "sz": 0.01, **lit(DIM, 0.035)},
            fig,
        ],
        "filters": [{"type": "fence", "n": C, "slide": f"{T}*{C}", "width": 0.0056, "fence": 0.76,
                     # A long riff is many pictures and few gaps: wider gaps keep it bright (two pictures show at once).
                     "gap": f"clamp({C}/4.5, 1.4, 2.8)", "gain": f"min(1.2 + 0.4*{C}, 5)"}],
    }


def fence(tracks, spot, spot_track=None, subject="horse", plain=()):
    """One or two lanes, each a riff under its own fence: a five's fence has a gap every five
    strips and a seven's every seven, and both slide at the one pulse. The whole turn of each
    riff is on its plate at once. Horses only: a body cut into strips must be solid to read."""
    tracks = tracks[:2]
    if SUBJECTS[subject][0] != "horse":
        subject = "horse"
    n = len(tracks)
    lane = (2 * HALF_H - 0.9) / n
    env, plates = {}, []
    if n > 1:
        env["all"] = {"when": together(tracks, plain), "decay": 2.4}
    for i, t in enumerate(tracks):
        col = spot if t == spot_track else INK
        y = (HALF_H - 0.25) - (i + 0.5) * lane
        plates.append({"type": "actor", "use": fence_look(t, col, subject, celled=t not in plain, y=round(y, 3), tall=round(min(0.78 * lane, 2.3), 3)), "key": 0, "mask": "none"})
    marks = border(spot) if n > 1 else []
    return {"env": env, "background": BLACK, "camera": CAM, "layers": backdrop() + plates + ruler() + marks, "filters": finish(spot)}


# ───────────────────────── the strip (a photo-finish of the riffs) ─────────────────────────

def strip(tracks, spot, spot_track=None, bars=4, plain=()):
    """The slit camera. Each track is a lamp riding up and down once per cell at the slit; the
    film runs past, so each lamp draws a wave whose length is its cell, beaded where its notes
    fall. Every bar line flashes at the slit: common time ruled across the odd waves."""
    n = len(tracks)
    xs = 2.6     # the slit, in the world
    layers = []
    for i, t in enumerate(tracks):
        y0 = (1.75 - 3.5 * (i + 0.5) / n) if n > 1 else 0
        amp = min(0.62, 1.5 / n)
        col = spot if t == spot_track else INK
        T, C = clock(t, t not in plain), teeth(t, t not in plain)
        # The lane's rails: threads at the top, middle and foot of the lamp's travel. Standing
        # still at the slit, they are drawn out as lines the whole length of the strip.
        for dy, lev in ((amp, 0.3), (0, 0.18), (-amp, 0.3)):
            layers.append({"type": "mesh", "shape": "box", "round": 0.02, "detail": 2, "x": xs + 1.2, "y": round(y0 + dy, 3), "z": 0.3, "scale": 1,
                           "sx": 1.25, "sy": 0.004, "sz": 0.004, **lit(DIM, lev)})
        # The lamp at the slit. It is drawn as tall as it travels in a thirtieth of a second, so
        # the strip shows an unbroken line however fast the lamp goes.
        run = f"{amp:.3f}*6.283*abs(sin({T}))*8*time.bpm/max({C}, 1)/30"
        layers.append({"type": "mesh", "shape": "sphere", "detail": 10, "x": xs, "y": f"{y0:.3f} + {amp:.3f}*cos({T})", "z": 0,
                       "scale": f"(0.03 + 0.06*track.{t}.hit)*(0.25 + 0.75*step(0.5, {C}))", "sy": f"1 + 0.5*({run})/(0.03 + 0.06*track.{t}.hit)", **lit(col, 1.2)})
        # The lamp's wheel, beyond the slit: what the strip is a photograph of.
        layers.append({"type": "shape", "sides": 0, "radius": round(amp * K, 4), "width": 0.006, "x": round((xs + amp + 0.25) * K, 4), "y": round(y0 * K, 4), "color": DIM, "opacity": 0.6})
        layers.append({"type": "mesh", "shape": "sphere", "detail": 10, "x": f"{xs + amp + 0.25:.3f} + {amp:.3f}*sin({T})", "y": f"{y0:.3f} + {amp:.3f}*cos({T})", "z": 0,
                       "scale": f"0.04 + 0.05*track.{t}.hit", **lit(col, 1.2)})
    # The bar line and the beats: a full line on the bar, a short tick on each beat.
    layers.append({"type": "mesh", "shape": "box", "round": 0.02, "detail": 2, "x": xs, "y": 0, "z": 0.2, "scale": 1, "sx": 0.03, "sy": 2.45, "sz": 0.006,
                   "opacity": "step(0.02, env.bar)", **lit(DIM, 0.55)})
    layers.append({"type": "mesh", "shape": "box", "round": 0.02, "detail": 2, "x": xs, "y": -2.3, "z": 0.2, "scale": 1, "sx": 0.03, "sy": 0.12, "sz": 0.006,
                   "opacity": "step(0.02, env.beat)", **lit(DIM, 0.8)})
    env = {"bar": {"on": "bar", "attack": "0ms", "decay": "45ms"}, "beat": {"on": "beat", "attack": "0ms", "decay": "45ms"}}
    if n > 1:
        # Where every lamp starts its cell at once: a line in the spot colour, ruled by the
        # riffs themselves wherever their cycles meet.
        env["all"] = {"when": together(tracks, plain), "decay": 0.06}
        layers.append({"type": "mesh", "shape": "box", "round": 0.02, "detail": 2, "x": xs, "y": 0, "z": 0.1, "scale": 1, "sx": 0.03, "sy": 2.45, "sz": 0.006,
                       "opacity": "step(0.02, env.all)", **lit(spot, 1.5)})
    return {
        "background": BLACK, "camera": CAM,
        "env": env,
        "layers": layers,
        # 4 bars across the whole frame: bars a second are time.bpm/2.
        "filters": [{"type": "slit", "x": round(xs * K, 4), "speed": f"time.bpm/{2*bars}"}] + finish(spot),
    }


# ───────────────────────── the walkers (Marey's plate) ─────────────────────────

# What is studied: (rig, motion, how tall it stands for scale 1, how thick its limbs are drawn,
# strides per turn of the cell, the turn about y that shows it from the side).
SUBJECTS = {
    # rig, motion, height (world units at scale 1, twice the origin's height above the feet),
    # thickness, stride cycles per `time.beat/…` turn, the turn that shows it side-on going right.
    "walker": ("human", "walk", 2.1, 0.32, 2, 0.25),
    "runner": ("human", "run", 2.1, 0.32, 2, 0.25),
    "dancer": ("human", "dance", 2.1, 0.32, 2, 0.04),
    "horse": ("horse", "gallop", 1.7, 0.85, 2, 0.0),
    "pacer": ("horse", "walk", 1.7, 0.85, 2, 0.0),
    "bird": ("bird", "flap", 0.9, 0.22, 2, 0.06),
}


def horse_bones():
    """A horse, as bones: built here (the engine's own quadruped is a table with a neck), so it
    needs nothing the engine does not already have. It stands along +x, about 1.4 high."""
    out = []

    def b(name, parent, length, d, w):
        out.append({"name": name, "parent": parent, "length": length, "dir": d, "width": w})

    b("hip", None, 0.02, [-1, 0, 0], 0.125)
    b("back", "hip", 0.74, [1, 0.03, 0], 0.14)
    b("neck", "back", 0.45, [0.6, 0.8, 0], 0.085)
    b("head", "neck", 0.28, [0.85, -0.53, 0], 0.062)
    b("tail", "hip", 0.14, [-0.85, 0.25, 0], 0.035)
    b("tail2", "tail", 0.4, [-0.55, -0.83, 0], 0.028)
    for side, z in (("l", -0.2), ("r", 0.2)):
        b(f"arm_{side}", "back", 0.40, [0.04, -1, z], 0.058)
        b(f"fore_{side}", f"arm_{side}", 0.34, [0, -1, 0], 0.034)
        b(f"hoof_{side}", f"fore_{side}", 0.07, [0.5, -0.85, 0], 0.03)
        b(f"thigh_{side}", "hip", 0.32, [0.3, -1, z], 0.078)
        b(f"gaskin_{side}", f"thigh_{side}", 0.30, [-0.38, -1, 0], 0.045)
        b(f"cannon_{side}", f"gaskin_{side}", 0.26, [0.1, -1, 0], 0.032)
    return out


def horse_pose(gait="gallop"):
    """The horse's gaits, one stride every two of its own beats. The gallop gathers and
    stretches (fore and hind legs against each other, each pair a little apart); the walk
    puts down one foot after another, four to the stride."""
    g = "time.beat/2"

    def z(e):
        return [0, 0, e]

    if gait == "gallop":
        pose = {
            "back": z(f"0.012*sin({g} + 0.3)"),
            "neck": z(f"0.025*sin({g} + 0.05)"),
            "head": z(f"0 - 0.03*sin({g} + 0.05)"),
            "tail2": z(f"0 - 0.12 + 0.03*sin({g})"),
        }
        for side, o in (("l", 0.0), ("r", 0.07)):
            pose[f"arm_{side}"] = z(f"0.13*sin({g} + {o})")
            pose[f"fore_{side}"] = z(f"0 - 0.17*max(0, cos({g} + {o}))")
            pose[f"hoof_{side}"] = z(f"0 - 0.1*max(0, cos({g} + {o}))")
            pose[f"thigh_{side}"] = z(f"0.12*sin({g} + 0.5 + {o})")
            pose[f"gaskin_{side}"] = z(f"0 - 0.06*max(0, cos({g} + 0.5 + {o}))")
            pose[f"cannon_{side}"] = z(f"0.14*max(0, cos({g} + 0.5 + {o}))")
        return pose
    pose = {"neck": z(f"0.012*sin(2*{g})"), "head": z(f"0 - 0.012*sin(2*{g})"), "tail2": z(f"0.02*sin({g})")}
    for name, o in (("thigh_l", 0.0), ("arm_l", 0.25), ("thigh_r", 0.5), ("arm_r", 0.75)):
        pose[name] = z(f"0.06*sin({g} + {o})")
        pose[name.replace("thigh", "gaskin").replace("arm", "fore")] = z(f"0 - 0.07*max(0, cos({g} + {o}))")
        if "thigh" in name:
            pose[name.replace("thigh", "cannon")] = z(f"0.1*max(0, cos({g} + {o}))")
    return pose


def subject_layer(subject, turn, hit, color, **place):
    """A subject's figure, its stride worked by `turn` (so many strides a turn)."""
    rig, motion, _, thick, strides, ry = SUBJECTS[subject]
    fig = {"type": "figure", "phase": f"{strides}*{turn} - time.beat", "thick": thick, "color": color,
           "emit": f"0.9 + 0.6*{hit}", "light": 0.2, "ambient": 0.9, "rim": 0, "ry": ry, **place}
    if rig == "horse":
        fig.update({"bones": horse_bones(), "motion": "none", "pose": horse_pose(motion)})
    else:
        fig["rig"] = rig
        if motion:
            fig["motion"] = motion
    return fig


def walker_look(track, color=INK, fade="20/time.bpm", live=0.3, subject="walker", celled=True, each=0.05):
    """One walker for one track, on its own plate. Common time carries it across (once every
    `param.across` bars); its own cell works its legs (a stride, two steps, for every turn);
    and every note is a flash. So the plate holds a row of the walker, spaced as the riff's
    notes are in time, each caught at the moment of the stride its cell had reached: two riffs
    of different lengths make rows that never quite repeat the same way. params: y (the lane's
    ground), size, across (bars to cross the frame), lead (where it starts, 0..1)."""
    T = clock(track, celled)
    return {
        "params": {"y": 0, "size": 0.6, "across": 4, "lead": 0},
        "background": BLACK,
        "camera": CAM,
        "layers": [
            # The ground line and its measure: a tick every half unit.
            {"type": "mesh", "shape": "box", "round": 0.02, "detail": 2, "x": 0, "y": "param.y - 0.02", "z": 0, "scale": 1, "sx": 4.4, "sy": 0.006, "sz": 0.006, **lit(DIM, 0.5)},
            {"type": "mesh", "shape": "box", "round": 0.02, "detail": 2, "count": 18, "x": "-4.25 + inst.i*0.5", "y": "param.y - 0.07", "z": 0, "scale": 1,
             "sx": 0.006, "sy": "0.03 + 0.03*step(fract(inst.i/4), 0.1)", "sz": 0.006, **lit(DIM, 0.5)},
            subject_layer(subject, T, f"track.{track}.hit", color, x="-4.7 + 9.4*fract(time.bar/param.across + param.lead)",
                          y=f"param.y + {SUBJECTS[subject][2] / 2:.2f}*param.size", z=0, scale="param.size"),
        ],
        "filters": [{"type": "expose", "on": f"track.{track}", "fade": fade, "each": each, "live": live}],
    }


def walkers(tracks, spot, spot_track=None, subject="walker", plain=()):
    """Up to three walkers, one above another, each a track, each on its own plate."""
    tracks = tracks[:3]
    n = len(tracks)
    tall = SUBJECTS[subject][2]
    horse = SUBJECTS[subject][0] == "horse"
    size = ({1: 3.0, 2: 2.0, 3: 1.35}[n] if horse else {1: 4.0, 2: 2.2, 3: 1.5}[n]) / tall
    layers = []
    for i, t in enumerate(tracks):
        y = (HALF_H - 0.2) - (i + 1) * (2 * HALF_H - 0.3) / n
        col = spot if t == spot_track else INK
        # A horse is long: it crosses in two bars, not four, and its prints fade sooner.
        look = walker_look(t, col, subject=subject, celled=t not in plain, fade="10/time.bpm" if horse else "20/time.bpm", each=0.09 if horse else 0.05)
        layers.append({"type": "actor", "use": look, "params": {"y": round(y, 3), "size": round(size, 3), "across": 2 if horse else 4, "lead": round(0.37 * i, 2)}, "key": 0, "mask": "none"})
    return {"background": BLACK, "camera": CAM, "layers": backdrop() + layers, "filters": finish(spot)}


# ───────────────────────── the sheet (Muybridge's row of cameras) ─────────────────────────

def sheet(tracks, spot, spot_track=None, subject="walker", plain=()):
    """A sequence sheet with as many panels as the first track's cell has sixteenths, one taken
    every sixteenth: so each panel always holds the same moment of the riff, and the sheet
    stands still while the riff repeats (a stride frozen into its frames, bright in the
    panels where the notes fall). A riff of eleven is eleven pictures, the twelfth place
    empty. The other tracks are beads that circle through it at their own lengths, so they
    are somewhere else in every panel each time round.
    People stand in tall panels (a row, or two); horses in wide ones (two rows to four)."""
    t0 = tracks[0]
    T = clock(t0, t0 not in plain)
    c = teeth(t0, t0 not in plain)
    wide = SUBJECTS[subject][0] == "horse"
    tall = SUBJECTS[subject][2]
    if wide:
        rows = f"(1 + step(2.5, {c}) + step(8.5, {c}) + step(15.5, {c}))"
    else:
        rows = f"(1 + step(8.5, {c}))"
    cols = f"max(floor((max({c}, 2) + {rows} - 1)/{rows}), 2)"
    if wide:
        # As big as its panel lets it be: a panel shows 9.08*rows/cols units across.
        size, ground = f"min(3.3, 4.1*{rows}/{cols})", -1.5
    else:
        size, ground = round(3.3 / tall, 3), -1.7
    layers = [
        {"type": "mesh", "shape": "box", "round": 0.02, "detail": 2, "x": 0, "y": ground - 0.02, "z": 0, "scale": 1, "sx": 4.6, "sy": 0.008, "sz": 0.008, **lit(DIM, 0.5)},
        {**subject_layer(subject, T, f"track.{t0}.hit", INK, x=f"0 - 0.27*({size})" if wide else 0, y=f"{ground} + {tall / 2}*({size})", z=0, scale=size),
         "emit": f"0.35 + 1.3*track.{t0}.hit"},
    ]
    # The other tracks: a bead each, circling above once per its own cell.
    for i, t in enumerate(tracks[1:4]):
        col = spot if t == spot_track else DIM
        r = 0.55 + 0.22 * i
        cy = 1.55 if wide else 1.2
        layers.append({"type": "mesh", "shape": "sphere", "detail": 10, "x": f"{r:.2f}*sin({clock(t, t not in plain)})", "y": f"{cy} + {r:.2f}*cos({clock(t, t not in plain)})", "z": 0.3,
                       "scale": f"0.04 + 0.07*track.{t}.hit", **lit(col, 1.3)})
    return {
        "background": BLACK, "camera": CAM, "layers": backdrop(0.2) + layers,
        "filters": [
            {"type": "panels", "cols": cols, "rows": rows, "count": f"max({c}, 2)", "every": 0.25, "gap": 0.014, "flash": 0.12, "border": "#000000"},
        ] + finish(spot),
    }


# ───────────────────────── the loops (a lamp left open) ─────────────────────────

def loops(tracks, spot, spot_track=None, plain=(), cells=None, shadow=True):
    """A lamp on an open shutter, and the wire model made from its path (Gilbreth's
    chronocyclegraphs). The lamp is swung across by one riff, up and down by the next and in
    and out by a third (or by the bar, where there are two), once per turn of each: so riffs
    of different lengths tie a knot, and the knot is the same for as long as they repeat. The
    lamp runs along it; behind it the last few bars of its path stand as a wire, in a box
    that turns slowly to show its depth. A riff that rests lets its side of the box go flat.
    Where the riffs all begin together the lamp is at the box's centre, going out along the
    long diagonal: nothing says so but the border."""
    ts = list(tracks[:3])
    cells = [c for c in (cells or [])[:3] if c] or [16]
    R, RY, Y0 = 1.8, 1.42, 0.2
    back = "(var.nowb - time.beat)*4"            # sixteenths back along the wire
    rot = "(var.nowb/112 + 0.06)"                # the box turns once in twenty-eight bars
    # Each riff's length as it is now; where the engine finds none, or a stutter of one or
    # two, the length it has for most of this stretch.
    live = [("16" if t in plain else f"mix({c}, track.{t}.cell, step(2.5, track.{t}.cell))") for t, c in zip(ts, cells + [16] * 3)]
    then = [("time.bar" if t in plain else f"(track.{t}.turn - {back}/{c})") for t, c in zip(ts, live)]
    now = [clock(t, t not in plain) for t in ts]
    amp = [f"(0.12 + 0.88*var.lv{i})" for i in range(len(ts))]
    while len(then) < 3:                         # common time is the depth
        then.append("time.bar"), now.append("time.bar"), amp.append("0.6")

    def spin(x, y, z):
        """A point of the box, turned with it."""
        return (f"({x})*cos({rot}) + ({z})*sin({rot})", f"{Y0} + {y}", f"({z})*cos({rot}) - ({x})*sin({rot})")

    def path(a, flat=None):
        pt = [f"{R}*{amp[0]}*sin({a[0]})", f"{RY}*{amp[1]}*sin({a[1]})", f"{R}*{amp[2]}*sin({a[2]})"]
        if flat is not None:
            pt[flat[0]] = str(flat[1])
        return spin(*pt)

    whole = 1
    for c in cells:
        whole = whole * c // math.gcd(whole, c)
    # Sixteenths of wire: the whole knot if it closes within five bars; if not, five bars
    # of it, or four turns of the longest riff.
    length = min(whole, max(80, 4 * max(cells)), 176)
    least = live[0]
    for c in live[1:]:
        least = f"min({least}, {c})"
    n = f"clamp({length * 44}/{least}, 96, 2000)"    # forty-four points to a turn of the shortest riff
    tx, ty, tz = path(then)
    hx, hy, hz = path(now)
    hit = " + ".join(f"track.{t}.hit" for t in ts)
    wire = {"type": "trail", "x": tx, "y": ty, "z": tz, "length": f"{length * 0.125:.4f}/time.bpm", "samples": n,
            "width": 0.021, "taper": 0.45, "glow": "0.75 + 0.5*audio.level", "fade": 0.82, "color": INK}
    layers = backdrop(z=3.0)                     # the wall stands clear behind the box's far corner
    # The box: twelve edges, four along each axis.
    s1, s2 = "(4*fract(inst.i/2) - 1)", "(2*floor(inst.i/2) - 1)"
    for ax in range(3):
        lo, hi = [None] * 3, [None] * 3
        o1, o2 = [k for k in range(3) if k != ax]
        ext = [R, RY, R]
        for pt, sign in ((lo, -1), (hi, 1)):
            pt[ax] = f"{sign * ext[ax]}"
            pt[o1] = f"{ext[o1]}*{s1}"
            pt[o2] = f"{ext[o2]}*{s2}"
        layers.append({"type": "beam", "count": 4, "from": list(spin(*lo)), "to": list(spin(*hi)), "samples": 24, "width": 0.006, "glow": 0.5, "color": DIM})
    if shadow:
        # Its shadow on the box's floor: the figure two of the riffs make by themselves.
        fx, fy, fz = path(then, flat=(1, -RY))
        layers.append({"type": "trail", "x": fx, "y": fy, "z": fz, "length": f"{length * 0.125:.4f}/time.bpm", "samples": n,
                       "width": 0.01, "taper": 0.3, "glow": 0.3, "fade": 0.7, "color": DIM})
    layers += [
        wire,
        {"type": "mesh", "shape": "sphere", "detail": 12, "x": hx, "y": hy, "z": hz, "scale": f"0.055 + 0.06*min({hit}, 1)", **lit(spot, 1.8)},
    ]
    env, marks = {}, []
    if len(ts) > 1:
        env["all"] = {"when": together(ts, plain), "decay": 2.4}
        marks = border(spot)
    return {
        "vars": {"nowb": {"follow": "time.beat", "attack": "0ms", "release": "0ms"},
                 **{f"lv{i}": {"follow": "1" if t in plain else f"clamp(track.{t}.level*8, 0, 1)", "attack": "250ms", "release": "1800ms"} for i, t in enumerate(ts)}},
        "env": env, "background": BLACK, "camera": CAM,
        "layers": layers + ruler() + marks,
        "filters": finish(spot),
    }


# ───────────────────────── the tracer (a tune drawn by its lamp) ─────────────────────────

def tracer(tracks, spot, spot_track=None, bars=2):
    """A lamp for each tune: it crosses the plate once every two bars and stands as high as the
    note it plays, lit only while the note sounds; the plate is left open, so the tune draws
    its own line and the last few passes hang under it, fading."""
    layers = []
    for i, t in enumerate(tracks[:3]):
        col = spot if (t == spot_track or len(tracks) == 1) else INK
        layers.append({"type": "mesh", "shape": "sphere", "detail": 10, "x": f"-4.1 + 8.2*fract(time.bar/{bars})",
                       "y": f"-1.7 + 3.6*clamp((track.{t}.key - param.lo{i})/max(param.hi{i} - param.lo{i}, 0.01), 0, 1)", "z": 0,
                       "scale": f"0.03 + 0.05*track.{t}.hit", "opacity": f"step(0.5, track.{t}.gate)", **lit(col, 1.3)})
    return {
        "params": {f"{k}{i}": v for i in range(3) for k, v in (("lo", 0.2), ("hi", 0.7))},
        "background": BLACK, "camera": CAM, "layers": layers + ruler(),
        "filters": [{"type": "expose", "fade": f"{2*bars*1.5}/time.bpm", "live": 1.0}] + finish(spot),
    }


# ───────────────────────── the studio (where the plates are made) ─────────────────────────

def negative(color):
    """A colour's negative: what to draw so that a print turned over shows `color`."""
    v = int(color.lstrip("#"), 16)
    return f"#{0xffffff - v:06x}"


def studio(tracks, spot, spot_track=None, subject="walker", plain=(), white=False):
    """The track itself, in daylight: a black wall ruled in white threads, a pale floor, and the
    walkers in white going along it, one per track, each striding to its own cell. Real light:
    a sky, shadows from the sun, contact shade. The camera tracks slowly along the wall."""
    tracks = tracks[:4]
    n = len(tracks)
    rig, motion, tall, thick, strides, ry = SUBJECTS[subject]
    if white:
        spot = negative(spot)     # the song's ink, as it prints
    layers = [
        {"type": "sky", "zenith": "#4a4a4c", "horizon": "#c4c2bc", "ground": "#5a5852", "sun": "#fff4e0", "sun_yaw": -0.14, "sun_height": 0.16, "sun_size": 0.03,
         "glow": 0.5, "haze": 0.5, "clouds": 0.6, "cloud_height": 6, "cloud_scale": 0.12},
        # The floor: pale.
        {"type": "mesh", "shape": "plane", "detail": 4, "x": 0, "y": 0, "z": 0, "scale": 40, "material": "pbr", "rough": 0.95, "metal": 0, "color": "#6f6c66", "cull": True},
        # Chalk lines across the track, one a unit (thin boxes lying on the floor).
        {"type": "mesh", "shape": "box", "round": 0.02, "detail": 2, "count": 13, "x": "inst.i - 6", "y": 0.004, "z": -0.2, "scale": 1, "sx": 0.012, "sy": 0.003, "sz": 1.4,
         "color": "#d8d4ca", "light": 0.8, "ambient": 0.5, "rim": 0},
        # The wall: black, with white threads every half unit and a heavier one every two
        # (painted on: threads as separate bodies would each be drawn again for the shadows).
        {"type": "mesh", "shape": "box", "round": 0.01, "detail": 2, "x": 0, "y": 1.6, "z": 1.3, "scale": 1, "sx": 30, "sy": 1.6, "sz": 0.05, "color": "#0b0b0b", "light": 0.5, "ambient": 0.3, "rim": 0,
         "paint_fine": True, "paint_color": "#e8e4da",
         "paint": "step(0.97, fract(vtx.x*60 + 0.5))*0.5 + step(0.97, fract(vtx.y*3.2 + 0.5))*0.5 + step(0.985, fract(vtx.x*15 + 0.5))*0.5"},
    ]
    for i, t in enumerate(tracks):
        z = 0.55 - 0.5 * i
        col = spot if t == spot_track else "#e9e6df"
        T = clock(t, t not in plain)
        # Common time carries each across; its own cell works its legs. Behind it, where it was
        # a moment ago and a moment before that: the plate, standing in the daylight.
        fig = subject_layer(subject, T, f"track.{t}.hit", col, x=f"-4.6 + 9.2*fract(time.bar/{5 + 2*i} + {0.27*i:.2f})", y=round(tall * 0.9 / 2, 3), z=z, scale=0.9)
        fig.update({"thick": 1.0, "melt": 0.05, "light": 1.0, "ambient": 0.2, "material": "pbr", "rough": 0.8, "metal": 0,
                    "emit": f"{0.75 if t == spot_track else 0.5} + 0.35*track.{t}.hit", "echo": 4, "echo_gap": "0.25/time.bpm"})
        layers.append(fig)
    return {
        "background": "#d8d5ce",
        "camera": {"x": "1.6*sin(time.bar/32)", "y": 0.95, "z": -3.9, "look_at": ["1.0*sin(time.bar/32)", 0.8, 0.6], "zoom": 1.3},
        "layers": layers,
        "filters": [
            {"type": "shadowmap", "amount": 0.55, "soft": 2, "size": 1024},
            {"type": "ao", "amount": 0.6, "radius": 0.05},
            {"type": "tonemap", "knee": 0.8},
            {"type": "color", "contrast": 1.08},
            {"type": "aa"},
            # In a song printed as a negative the studio is still daylight: turned over here, it
            # comes out the right way through the master.
        ] + ([{"type": "invert"}] if white else []),
    }


def chase(tracks, spot, spot_track=None, subject="horse", plain=(), white=False):
    """The studio again, with the camera running alongside: the wall's threads stream past at
    common time's own pace while the runners hold their places in the picture, each one's legs
    going at its own cell and each surging and falling back once a turn, so they race without
    any of them ever winning. Their earlier poses trail out behind them."""
    tracks = tracks[:3]
    rig, motion, tall, thick, strides, ry = SUBJECTS[subject]
    horse = rig == "horse"
    if white:
        spot = negative(spot)
    v = 3.0 if horse else 2.0                # units a bar
    # How far the camera has run: so many units a bar since the scene began (places in the
    # world stay small, and the earlier poses are truly behind).
    cam = f"({v / 2}*scene.t*time.bpm)"
    layers = [
        {"type": "sky", "zenith": "#4a4a4c", "horizon": "#c4c2bc", "ground": "#5a5852", "sun": "#fff4e0", "sun_yaw": -0.14, "sun_height": 0.16, "sun_size": 0.03,
         "glow": 0.5, "haze": 0.5, "clouds": 0.6, "cloud_height": 6, "cloud_scale": 0.12},
        {"type": "mesh", "shape": "plane", "detail": 4, "x": cam, "y": 0, "z": 0, "scale": 40, "material": "pbr", "rough": 0.95, "metal": 0, "color": "#6f6c66", "cull": True},
        # Chalk lines and the wall keep their places in the world: each is put down again a
        # whole step ahead as the camera passes, so they stream by without end.
        {"type": "mesh", "shape": "box", "round": 0.02, "detail": 2, "count": 13, "x": f"inst.i - 6 + floor({cam})", "y": 0.004, "z": -0.2, "scale": 1, "sx": 0.012, "sy": 0.003, "sz": 1.6,
         "color": "#d8d4ca", "light": 0.8, "ambient": 0.5, "rim": 0},
        {"type": "mesh", "shape": "box", "round": 0.01, "detail": 2, "x": f"2*floor({cam}/2)", "y": 1.6, "z": 1.3, "scale": 1, "sx": 30, "sy": 1.6, "sz": 0.05, "color": "#0b0b0b", "light": 0.5, "ambient": 0.3, "rim": 0,
         "paint_fine": True, "paint_color": "#e8e4da",
         "paint": "step(0.97, fract(vtx.x*60 + 0.5))*0.5 + step(0.97, fract(vtx.y*3.2 + 0.5))*0.5 + step(0.985, fract(vtx.x*15 + 0.5))*0.5"},
    ]
    size = 1.0 if horse else 0.95
    for i, t in enumerate(tracks):
        col = spot if t == spot_track else "#e9e6df"
        T = clock(t, t not in plain)
        x = f"{cam} + {(i - (len(tracks) - 1) / 2) * (1.5 if horse else 1.0):.2f} + 0.35*sin({T} + {0.3*i:.2f})"
        fig = subject_layer(subject, T, f"track.{t}.hit", col, x=x, y=round(tall * size / 2, 3), z=round(0.55 - 0.6 * i, 2), scale=size)
        fig.update({"thick": 1.0, "melt": 0.05, "light": 1.0, "ambient": 0.2, "material": "pbr", "rough": 0.8, "metal": 0,
                    "emit": f"{0.75 if t == spot_track else 0.5} + 0.35*track.{t}.hit", "echo": 4, "echo_gap": "0.25/time.bpm"})
        layers.append(fig)
    return {
        "background": "#d8d5ce",
        "camera": {"x": f"{cam} + 0.5*sin(time.bar/16)", "y": 0.85, "z": -4.4, "look_at": [f"{cam} + 0.2", 0.66, 0.5], "zoom": 1.5},
        "layers": layers,
        "filters": [
            {"type": "shadowmap", "amount": 0.55, "soft": 2, "size": 1024},
            {"type": "ao", "amount": 0.6, "radius": 0.05},
            {"type": "tonemap", "knee": 0.8},
            {"type": "color", "contrast": 1.08},
            {"type": "aa"},
        ] + ([{"type": "invert"}] if white else []),
    }


# ───────────────────────── the flight (a tune as a bird) ─────────────────────────

def flight_look(track, color=INK, bars=2, fade=None, lo=0.3, hi=0.7, phase=0.0):
    """One bird for one tune, on its own plate: it crosses once every `bars` bars, flies as high
    as the note it sings, beats its wings once a beat, and is flashed by each note, so the
    plate holds the tune as a row of birds at the heights of its notes (Marey's gull)."""
    key = f"clamp((track.{track}.key - {lo:.3f})/{max(hi - lo, 0.02):.3f}, 0, 1)"
    return {
        "params": {"size": 1.0},
        "background": BLACK, "camera": CAM,
        # The height glides to each note rather than jumping.
        "vars": {"h": {"follow": key, "attack": "70ms", "release": "70ms"}},
        "layers": [
            {"type": "figure", "rig": "bird", "motion": "flap", "phase": 0, "thick": 0.22, "color": color,
             "x": f"-4.7 + 9.4*fract(time.bar/{bars} + {phase:.2f})", "y": "-1.6 + 3.3*var.h", "z": 0, "ry": 0.06, "scale": "param.size",
             "emit": f"0.9 + 0.7*track.{track}.hit", "light": 0.2, "ambient": 0.9, "rim": 0},
        ],
        "filters": [{"type": "expose", "on": f"track.{track}", "fade": fade or f"{8*bars:g}/time.bpm", "each": 0.06, "live": 0.45}],
    }


def flight(tracks, spot, spot_track=None, ranges=None, bars=2):
    """Up to three tunes as birds over the ruled plate; `ranges` gives each track's lowest and
    highest note (as track.T.key reads them, 0..1) so each bird uses the whole height."""
    tracks = tracks[:3]
    layers = []
    for i, t in enumerate(tracks):
        lo, hi = (ranges or {}).get(t, (0.3, 0.7))
        col = spot if (t == spot_track or len(tracks) == 1) else INK
        layers.append({"type": "actor", "use": flight_look(t, col, bars=bars, lo=lo, hi=hi, phase=0.31 * i), "params": {"size": {1: 1.5, 2: 1.2, 3: 1.0}[len(tracks)]}, "key": 0, "mask": "none"})
    return {"background": BLACK, "camera": CAM, "layers": backdrop() + layers + ruler(), "filters": finish(spot)}


# ───────────────────────── the pendulums (odd sympathy) ─────────────────────────

def pendulum_look(track, color=INK, celled=True, fade="16/time.bpm"):
    """One pendulum for one track, on its own plate: it swings out and back once per cell, and
    each note is a flash, so the plate holds the bob wherever in the swing the riff's notes
    fall: a fan with the riff's rhythm in it. params: cx (the pivot), top, length, swing."""
    T = clock(track, celled)
    ang = f"param.swing*sin({T})"            # turns from straight down
    bx = f"param.cx + param.length*sin({ang})"
    by = f"param.top - param.length*cos({ang})"
    return {
        "params": {"cx": 0, "top": 2.0, "length": 3.0, "swing": 0.09},
        "background": BLACK, "camera": CAM,
        "layers": [
            {"type": "mesh", "shape": "box", "round": 0.02, "detail": 2, "x": f"param.cx + 0.5*param.length*sin({ang})", "y": f"param.top - 0.5*param.length*cos({ang})", "z": 0,
             "rz": ang, "scale": "param.length*0.5", "sx": 0.008, "sy": 1, "sz": 0.008, **lit(DIM, 0.8)},
            {"type": "mesh", "shape": "sphere", "detail": 14, "x": bx, "y": by, "z": 0, "scale": f"0.14 + 0.06*track.{track}.hit", **lit(color, 1.3)},
            {"type": "mesh", "shape": "sphere", "detail": 8, "x": "param.cx", "y": "param.top", "z": 0, "scale": 0.035, **lit(DIM, 1.0)},
        ],
        "filters": [{"type": "expose", "on": f"track.{track}", "fade": fade, "each": 0.1, "live": 0.35}],
    }


def pendulums(tracks, spot, spot_track=None, plain=()):
    """Up to five pendulums hung from one beam, each a track, each as long as its cell is (a
    longer riff, a longer pendulum): they swing at their own lengths and fall in and out of
    step, as the clocks on Huygens's wall did."""
    tracks = tracks[:5]
    n = len(tracks)
    layers = [{"type": "mesh", "shape": "box", "round": 0.02, "detail": 2, "x": 0, "y": 2.05, "z": 0, "scale": 1, "sx": 4.3, "sy": 0.02, "sz": 0.02, **lit(DIM, 0.8)},
              # The beam lights when every pendulum swings through the middle at once.
              {"type": "mesh", "shape": "box", "round": 0.02, "detail": 2, "x": 0, "y": 2.05, "z": -0.05, "scale": 1, "sx": 4.3, "sy": 0.024, "sz": 0.02,
               "opacity": "env.all", **lit(spot, 1.6)}]
    for i, t in enumerate(tracks):
        x = (i - (n - 1) / 2) * min(2.6, 8.0 / n)
        col = spot if t == spot_track else INK
        layers.append({"type": "actor", "use": pendulum_look(t, col, celled=t not in plain),
                       "params": {"cx": round(x, 3), "top": 2.05, "length": f"1.6 + 2.4*sqrt(clamp({teeth(t, t not in plain)}/16, 0, 1))", "swing": 0.1}, "key": 0, "mask": "none"})
    return {"env": {"all": {"when": together(tracks, plain) if n > 1 else "0", "decay": 2.0}},
            "background": BLACK, "camera": CAM, "layers": backdrop() + layers + ruler() + border(spot), "filters": finish(spot)}


# ───────────────────────── the balls (Edgerton's strobe) ─────────────────────────

def ball_look(track, color=INK, celled=True, fade="8/time.bpm"):
    """One ball for one track, on its own plate: it bounces once per cell (a riff of eleven
    stays up longer than a riff of five, and so goes higher), common time carries it across,
    and each note is a flash. Between flashes the plate takes a little light all the time,
    so the arcs are there faintly and the notes are beads on them.
    params: floor, height (of a bounce), across (bars), lead, size."""
    T = clock(track, celled)
    p = f"fract({T})"
    return {
        "params": {"floor": -1.6, "height": 2.0, "across": 4, "lead": 0, "size": 0.09},
        "background": BLACK, "camera": CAM,
        "layers": [
            {"type": "mesh", "shape": "sphere", "detail": 14, "x": "-4.7 + 9.4*fract(time.bar/param.across + param.lead)",
             "y": f"param.floor + param.size + param.height*4*{p}*(1 - {p})", "z": 0,
             "scale": f"param.size*(1 + 0.5*track.{track}.hit)", **lit(color, 1.4)},
        ],
        "filters": [{"type": "expose", "on": f"track.{track}", "open": 0.2, "fade": fade, "live": 0.5}],
    }


def balls(tracks, spot, spot_track=None, plain=()):
    """Up to four balls dropped on one floor, each bouncing to its own riff. They land
    together only where the cycles meet, and the floor lights when they do."""
    tracks = tracks[:4]
    n = len(tracks)
    floor = -1.7
    layers = [
        {"type": "mesh", "shape": "box", "round": 0.02, "detail": 2, "x": 0, "y": floor - 0.02, "z": 0, "scale": 1, "sx": 4.6, "sy": 0.012, "sz": 0.02, **lit(DIM, 0.9)},
        {"type": "mesh", "shape": "box", "round": 0.02, "detail": 2, "x": 0, "y": floor - 0.02, "z": -0.05, "scale": 1, "sx": 4.6, "sy": 0.016, "sz": 0.02,
         "opacity": "env.all", **lit(spot, 1.6)},
    ]
    vars_ = {}
    longest = "0"
    for t in tracks:
        longest = f"max({longest}, min({teeth(t, t not in plain)}, 24))"
    for i, t in enumerate(tracks):
        col = spot if t == spot_track else INK
        C = teeth(t, t not in plain)
        # A bounce's height goes as the square of its time in the air, as a real one's does;
        # the longest riff among them has the full height.
        vars_[f"h{i}"] = {"follow": f"3.5*pow({C}/max({longest}, 4), 2)", "attack": "400ms", "release": "400ms"}
        layers.append({"type": "actor", "use": ball_look(t, col, celled=t not in plain),
                       "params": {"floor": floor, "height": f"clamp(var.h{i}, 0.4, 3.5)", "across": 4, "lead": round(0.21 * i, 2), "size": 0.07}, "key": 0, "mask": "none"})
    return {"vars": vars_, "env": {"all": {"when": together(tracks, plain) if n > 1 else "0", "decay": 1.6}},
            "background": BLACK, "camera": CAM, "layers": backdrop() + layers + ruler() + border(spot), "filters": finish(spot)}


# ───────────────────────── the finish (a photo-finish of the riffs) ─────────────────────────

def finish_line(tracks, spot, spot_track=None, subject="runner", bars=2, plain=(), meet=True):
    """The photo-finish camera, pointed at a finishing line. Each track has a lane and a
    runner who crosses the line once per cell, running at the speed the film does, so the
    strip holds each one whole, lane by lane, as far apart as its riff is long: fives in one
    lane, sevens in the next. Each runner crosses a little further through the stride than
    the last, so a lane reads along as a sequence. Standing things (the lane lines) are drawn
    out along the strip; a lamp over each lane marks its notes along the top, as a timing
    strip does; each bar is a hairline; and where the cycles meet the runners cross level (a
    dead heat) and the line is drawn in the spot colour."""
    tracks = tracks[:3]
    n = len(tracks)
    xs = 3.0                                  # the line, in the world
    v = 2 * HALF_W / (16 * bars)              # world units a sixteenth: the film's speed
    lane = (2 * HALF_H - 0.35) / n
    rig_h = SUBJECTS[subject][2]
    tall = min(0.74 * lane, 2.6)
    size = tall / rig_h
    layers = []
    vars_ = {}
    for i, t in enumerate(tracks):
        foot = (HALF_H - 0.1) - (i + 1) * lane
        col = spot if t == spot_track else INK
        celled = t not in plain
        T, C = clock(t, celled), teeth(t, celled)
        # A riff shorter than five sixteenths is counted in twos or threes, so a body still
        # fits; a very long one sends two or three runners a turn, so the lane is not bare.
        m = f"((1 + step({C}, 4.5) + step({C}, 2.5))/(1 + step(16.5, {C}) + step(32.5, {C})))"
        x = f"{xs} + (0.5 - fract(({T})/{m} + 0.5))*{v:.4f}*max({C}, 1)*{m}"
        # The lane's line: standing at the line, it is drawn out the length of the strip.
        layers.append({"type": "mesh", "shape": "box", "round": 0.02, "detail": 2, "x": xs + 0.9, "y": round(foot - 0.03, 3), "z": 0.3, "scale": 1,
                       "sx": 1.1, "sy": 0.006, "sz": 0.004, **lit(DIM, 0.5)})
        # The lane's lamp: lit on each note, so the notes are marked along the top of the lane.
        layers.append({"type": "mesh", "shape": "box", "round": 0.02, "detail": 2, "x": xs - 0.02, "y": round(foot + lane - 0.16, 3), "z": 0.1, "scale": 1,
                       "sx": 0.035, "sy": f"0.02 + 0.05*track.{t}.vel", "sz": 0.006, "opacity": f"step(0.5, track.{t}.hit)", **lit(col, 1.2)})
        fig = subject_layer(subject, T, f"track.{t}.hit", col, x=x, y=round(foot + rig_h / 2 * size, 3), z=0, scale=round(size, 3))
        fig["ry"] = -SUBJECTS[subject][5] if SUBJECTS[subject][5] else 0.5   # facing the way it runs: leftward
        # Not while its wheel stands (a rest, or a riff waiting to come round again): a body
        # standing on the line would be drawn out as a smear. The wheel is moving while it
        # is ahead of where it was a moment ago.
        # (A slow follower: it lags a turning wheel by a seventh of a second's turn at any
        # frame rate, and catches a standing one up. A quick one fell under the mark for
        # slow wheels, and long riffs in slow songs had no runners at all.)
        vars_[f"was{i}"] = {"follow": T, "attack": "150ms", "release": "150ms"}
        fig["opacity"] = f"step(0.5, {C})*step(0.003, {T} - var.was{i})"
        fig["emit"] = 1.1
        fig["thick"] = max(SUBJECTS[subject][3], 0.42)
        # Held in one pose while it crosses (so the film takes it clean), a little further
        # through the stride each time.
        fig["phase"] = f"0.3*floor(({T})/{m} + 0.5) - time.beat"
        layers.append(fig)
    env = {"bar": {"on": "bar", "attack": "0ms", "decay": "20ms"}}
    layers.append({"type": "mesh", "shape": "box", "round": 0.02, "detail": 2, "x": xs - 0.012, "y": 0, "z": 0.2, "scale": 1, "sx": 0.008, "sy": 2.5, "sz": 0.006,
                   "opacity": "step(0.6, env.bar)", **lit(DIM, 0.7)})
    if n > 1 and meet:
        # One frame long, so the film takes it once: a single line.
        env["all"] = {"when": together(tracks, plain), "decay": 0.02}
        layers.append({"type": "mesh", "shape": "box", "round": 0.02, "detail": 2, "x": xs - 0.012, "y": 0, "z": 0.1, "scale": 1, "sx": 0.012, "sy": 2.5, "sz": 0.006,
                       "opacity": "step(0.6, env.all)", **lit(spot, 1.5)})
    return {
        "background": BLACK, "camera": CAM, "vars": vars_, "env": env, "layers": layers,
        "filters": [{"type": "slit", "x": round(xs * K, 4), "speed": f"time.bpm/{2*bars}", "live": 0.8, "band": 1}] + finish(spot),
    }
