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


def finish(spot):
    """A plate's own finish: halation round the bright parts. (The print itself, its grain and
    dark corners, and whether it is a negative, belong to the song's master: see `master`.)"""
    return [{"type": "bloom", "threshold": 0.55, "amount": 0.35, "radius": 0.012}]


def master(number, title, white=False):
    """What lies over every scene of a song: the plate's label for its first seconds, and the
    print. `white`: the song is printed as a negative, black figures on a pale ruled wall (the
    spot colour turns to its complement, an ink)."""
    label = [
        # The plate is veiled while its name is up.
        {"type": "shape", "sides": 4, "radius": 4, "width": 0, "fill": 1, "color": "#3a3a3a", "blend": "multiply", "opacity": "1 - smooth(3.0, 4.4, time.bar)"},
        {"type": "text", "text": f"PLATE {number:02d}", "size": 0.05, "x": 0, "y": 0.2, "align": "center", "color": DIM, "width": 0.11, "skew": 0,
         "opacity": "smooth(0.1, 0.6, time.bar)*(1 - smooth(3.2, 4.2, time.bar))"},
        {"type": "text", "text": title.upper(), "size": 0.17, "x": 0, "y": -0.07, "align": "center", "color": INK, "width": 0.12, "skew": 0,
         "opacity": "1 - smooth(3.2, 4.2, time.bar)", "reveal": "smooth(0.3, 1.6, time.bar)"},
    ]
    filters = ([{"type": "invert"}, {"type": "color", "brightness": -0.05, "contrast": 0.94}] if white else []) + [
        {"type": "grain", "amount": 0.05},
        {"type": "vignette", "amount": 0.3 if white else 0.55},
    ]
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

def wheel_look(track, color=INK, fade="1.2", live=0.3, celled=True):
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
        "filters": [{"type": "expose", "on": f"track.{track}", "fade": fade, "live": live}],
    }


def wheel_rim(track, x, y, r, celled=True, color=DIM, glow="0"):
    """The wheel itself, standing in the scene (not on the plate): a hoop, a hub, and a tooth
    for every sixteenth of the cell, so the wheel has as many teeth as the riff is long.
    `r` may be an expression (a wheel that grows with its riff); `glow` lights the hoop."""
    C = teeth(track, celled)
    N = f"max({C}, 1)"
    return [
        {"type": "shape", "sides": 0, "radius": f"({r})*{K:.4f}", "width": 0.007, "x": round(x * K, 4), "y": round(y * K, 4), "color": color,
         "opacity": f"0.75 + 0.25*({glow})", "glow": f"0.18*({glow})"},
        {"type": "mesh", "shape": "box", "round": 0.02, "detail": 2, "count": 48,
         "opacity": f"step(inst.i + 0.5, {C})",
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
        plates.append({"type": "actor", "use": wheel_look(t, col, celled=t not in plain), "params": {"cx": x, "cy": cy, "r": f"var.r{i}"}, "key": 0, "mask": "rect"})
        if i + 1 < n:
            # The thread between this wheel and the next, lit when they come round together.
            env[f"m{i}"] = {"when": together(tracks[i:i + 2], plain), "decay": 1.2}
            x2 = xs[i + 1]
            layers.append({"type": "mesh", "shape": "box", "round": 0.02, "detail": 2, "x": (x + x2) / 2, "y": cy, "z": 0.1, "scale": 1,
                           "sx": (x2 - x) / 2, "sy": 0.006, "sz": 0.006, "opacity": f"env.m{i}", **lit(spot, 1.4)})
    return {"vars": vars_, "env": env, "background": BLACK, "camera": CAM, "layers": backdrop() + layers + plates + ruler(), "filters": finish(spot)}


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


def walker_look(track, color=INK, fade="8/time.bpm", live=0.3, subject="walker", celled=True):
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
        "filters": [{"type": "expose", "on": f"track.{track}", "fade": fade, "live": live}],
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
        look = walker_look(t, col, subject=subject, celled=t not in plain, fade="4/time.bpm" if horse else "8/time.bpm")
        layers.append({"type": "actor", "use": look, "params": {"y": round(y, 3), "size": round(size, 3), "across": 2 if horse else 4, "lead": round(0.37 * i, 2)}, "key": 0})
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

def loops(tracks, spot, spot_track=None):
    """Lamps on a long exposure. Each lamp is carried across by one track's wheel and up and
    down by the next one's, so two riffs of different lengths draw their own knot (five against
    seven is a figure of five lobes by seven); where they are the same length it is a ring.
    The lamp flares on its notes, so the path is beaded with them."""
    n = len(tracks)
    layers = []
    pairs = [(tracks[i], tracks[(i + 1) % n]) for i in range(min(n - 1, 2))] if n > 1 else [(tracks[0], tracks[0])]
    for i, (a, b) in enumerate(pairs):
        r = 2.0 - 0.75 * i
        col = spot if a == spot_track else INK
        layers.append({"type": "mesh", "shape": "sphere", "detail": 10, "x": f"{r*1.75:.2f}*sin(track.{a}.turn)", "y": f"{r:.2f}*cos(track.{b}.turn + {0.25 if a == b else 0})", "z": 0,
                       "scale": f"0.018 + 0.045*track.{a}.hit", **lit(col, "0.7 + 1.2*track.%s.hit" % a)})
    return {
        "background": BLACK, "camera": CAM, "layers": layers + ruler(),
        # A flash every eighth of a beat: the path is drawn in beads, eight to the beat, so the
        # odd loops can be counted in common time (two bars of them hang on the plate).
        "filters": [{"type": "expose", "every": 0.125, "fade": "5/time.bpm", "live": 1.0}] + finish(spot),
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
        # The floor: pale, ruled across every unit.
        {"type": "mesh", "shape": "plane", "detail": 4, "x": 0, "y": 0, "z": 0, "scale": 40, "material": "pbr", "rough": 0.95, "metal": 0, "color": "#6f6c66", "cull": True,
         # Chalk lines across the track, one a unit.
         "paint_fine": True, "paint_color": "#d8d4ca", "paint": "0.35*step(0.985, fract(vtx.x*40 + 0.5))*step(vtx.z*40, 1.2)*step(-1.6, vtx.z*40)"},
        # The wall: black, with white threads every half unit and a heavier one every two.
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
        fig = subject_layer(subject, T, f"track.{t}.hit", col, x=f"-5.5 + 11*fract(time.bar/{6 + 2*i} + {0.27*i:.2f})", y=round(tall * 0.9 / 2, 3), z=z, scale=0.9)
        fig.update({"thick": 1.0, "melt": 0.05, "light": 1.0, "ambient": 0.2, "material": "pbr", "rough": 0.8, "metal": 0,
                    "emit": f"{0.45 if t == spot_track else 0.05} + 0.3*track.{t}.hit", "echo": 5, "echo_gap": "0.25/time.bpm"})
        layers.append(fig)
    return {
        "background": "#d8d5ce",
        "camera": {"x": "1.6*sin(time.bar/32)", "y": 1.0, "z": -3.9, "look_at": ["1.0*sin(time.bar/32)", 0.95, 0.6], "zoom": 1.1},
        "layers": layers,
        "filters": [
            {"type": "shadowmap", "amount": 0.55, "soft": 2, "size": 1536},
            {"type": "ao", "amount": 0.6, "radius": 0.05},
            {"type": "tonemap", "knee": 0.8},
            {"type": "color", "contrast": 1.08},
            {"type": "aa"},
            # In a song printed as a negative the studio is still daylight: turned over here, it
            # comes out the right way through the master.
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
        "filters": [{"type": "expose", "on": f"track.{track}", "fade": fade or f"{4*bars:g}/time.bpm", "live": 0.45}],
    }


def flight(tracks, spot, spot_track=None, ranges=None, bars=2):
    """Up to three tunes as birds over the ruled plate; `ranges` gives each track's lowest and
    highest note (as track.T.key reads them, 0..1) so each bird uses the whole height."""
    tracks = tracks[:3]
    layers = []
    for i, t in enumerate(tracks):
        lo, hi = (ranges or {}).get(t, (0.3, 0.7))
        col = spot if (t == spot_track or len(tracks) == 1) else INK
        layers.append({"type": "actor", "use": flight_look(t, col, bars=bars, lo=lo, hi=hi, phase=0.31 * i), "params": {"size": {1: 1.5, 2: 1.2, 3: 1.0}[len(tracks)]}, "key": 0})
    return {"background": BLACK, "camera": CAM, "layers": backdrop() + layers + ruler(), "filters": finish(spot)}


# ───────────────────────── the pendulums (odd sympathy) ─────────────────────────

def pendulum_look(track, color=INK, celled=True, fade="1.6"):
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
        "filters": [{"type": "expose", "on": f"track.{track}", "fade": fade, "live": 0.35}],
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
                       "params": {"cx": round(x, 3), "top": 2.05, "length": f"1.6 + 2.4*sqrt(clamp({teeth(t, t not in plain)}/16, 0, 1))", "swing": 0.1}, "key": 0})
    return {"env": {"all": {"when": together(tracks, plain) if n > 1 else "0", "decay": 2.0}},
            "background": BLACK, "camera": CAM, "layers": backdrop() + layers + ruler(), "filters": finish(spot)}


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
                       "params": {"floor": floor, "height": f"clamp(var.h{i}, 0.4, 3.5)", "across": 4, "lead": round(0.21 * i, 2), "size": 0.07}, "key": 0})
    return {"vars": vars_, "env": {"all": {"when": together(tracks, plain) if n > 1 else "0", "decay": 1.6}},
            "background": BLACK, "camera": CAM, "layers": backdrop() + layers + ruler(), "filters": finish(spot)}


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
        fig["opacity"] = f"step(0.5, {C})"
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
        "background": BLACK, "camera": CAM, "env": env, "layers": layers,
        "filters": [{"type": "slit", "x": round(xs * K, 4), "speed": f"time.bpm/{2*bars}", "live": 0.8, "band": 1}] + finish(spot),
    }
