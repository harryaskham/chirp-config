"""wild: Common Time's second film. Many small machines, each built from the notes themselves.

Every idiom here is a function of a scene's context (`Cx`: who plays, each part's cell and
where its turns begin, the song's colours) that returns a look. Nothing is fixed to a song:
the generator (wildgen.py) deals them over the music as it finds it.

A part's CELL is the length of its repeating riff in sixteenths; common time is the bar's 16.
The idioms keep to one rule: what the music counts, the picture counts (a note is a thing, a
cell is a width, a turn is a turn), so the odd lengths are seen sliding against the bar.
"""
import math

REG = {}


def idiom(needs=1, fam="", paper=False, drums=False, tune=False, cost=1, min_bars=1, max_cell=64):
    """Register an idiom. needs: celled parts it wants (0: any music); fam: its family (no two
    of a family running); paper: it can be printed dark on light; cost: 1 cheap … 3 heavy."""
    def deco(f):
        REG[f.__name__] = dict(f=f, needs=needs, fam=fam or f.__name__, paper=paper, drums=drums, tune=tune, cost=cost, min_bars=min_bars, max_cell=max_cell)
        return f
    return deco


class P:
    """A part in a scene: its track, its cell (sixteenths; None: none), the sixteenth at which
    a turn of it begins, its pitch range here (MIDI) and its notes a bar."""
    def __init__(self, name, cell, anchor, role, lo, hi, rate, n=0):
        self.name, self.cell, self.anchor, self.role, self.lo, self.hi, self.rate = name, cell, anchor, role, lo, hi, rate
        self.n = n          # how many notes it plays in the scene

    # Expressions.
    @property
    def turn(self):
        """Turns of its riff since its anchor (unwrapped). A part that plays its riff ahead of
        another's (`lag`, an expression in sixteenths) is that much further on."""
        lag = getattr(self, "lag", None)
        return f"((time.beat*4 - {self.anchor:g}{' + (' + lag + ')' if lag else ''})/{self.cell or 16})"

    @property
    def ph(self):
        return f"fract({self.turn})"

    @property
    def nph(self):
        """A note's place in its riff, 0..1 (on a layer with notes: of this part)."""
        return f"fract((note.beat*4 - {self.anchor:g} + 0.01)/{self.cell or 16})"

    @property
    def nstep(self):
        """A note's place in its riff in sixteenths (whole)."""
        return f"floor({self.nph}*{self.cell or 16} + 0.02)"

    @property
    def hit(self):
        return f"track.{self.name}.hit"

    def pitch(self, lo=0.0, hi=1.0, src="note.midi"):
        """The note's pitch within this part's range here, mapped to lo..hi."""
        span = max(self.hi - self.lo, 1)
        return f"({lo:g} + {hi - lo:g}*clamp(({src} - {self.lo:g})/{span:g}, 0, 1))"


class Cx:
    def __init__(self, **kw):
        self.__dict__.update(kw)

    def r(self, i=0):
        """A fixed random number 0..1 for this scene (and i)."""
        x = math.sin((self.seed + 1) * 12.9898 + (i + 1) * 78.233) * 43758.5453
        return x - math.floor(x)

    def pick(self, seq, i=0):
        return seq[int(self.r(i) * len(seq)) % len(seq)]

    @property
    def tb(self):
        """Beats since the scene began."""
        return f"(time.beat - {self.a16 / 4:g})"

    @property
    def prog(self):
        """0..1 through the scene."""
        return f"clamp((time.beat - {self.a16 / 4:g})/{(self.b16 - self.a16) / 4:g}, 0, 1)"

    def col(self, i):
        return (self.a, self.b, self.c, self.ink)[i % 4]

    @property
    def arr(self):
        """How far a treatment has come on, 0..1: all the way, unless this scene is one where
        it arrives (or leaves) on a turn of the riff part way through."""
        return getattr(self, "arrive", "1")

    def sub(self, i, k=1):
        """This scene as part i alone sees it (its colour first): for a picture within a picture."""
        import copy
        d = copy.copy(self)
        d.riffs = (self.riffs[i:i + k] or self.riffs[:1])
        rot = i % 3
        d.a, d.b, d.c = (self.a, self.b, self.c)[rot:] + (self.a, self.b, self.c)[:rot]
        d.seed = self.seed * 7 + i + 1
        d.variant = self.variant + i
        return d


NOTE16 = "fract(note.beat/4 + 0.0006)*16"       # a note's sixteenth within its bar (0..16)
NBAR = "floor(note.beat/4 + 0.0006)"            # the bar it is in


def n(v):
    return f"{v:g}" if v >= 0 else f"(0 - {-v:g})"


def bloom(c, amount=0.5, radius=0.02, threshold=0.55):
    return {"type": "bloom", "threshold": threshold, "amount": f"{amount} + {amount}*audio.low", "radius": radius}


def cam(x=0, y=0, z=-6, look=(0, 0, 0), zoom=1.6, **kw):
    return {"x": x, "y": y, "z": z, "look_at": list(look), "zoom": zoom, **kw}


def glow(color, emit=1.0):
    return {"color": color, "emit": emit, "light": 0, "ambient": 1, "rim": 0}


def solid(color, rough=0.6, metal=0.0):
    return {"color": color, "material": "pbr", "rough": rough, "metal": metal, "rim": 0}


FLAT = {"x": 0, "y": 0, "z": -9, "look_at": [0, 0, 0], "zoom": 2.2}     # the frame is 5.11 high, 9.09 wide at z = 0
FH, FW = 2.557, 4.545


def box(x, y, z, sx, sy, sz, **kw):
    return {"type": "mesh", "shape": "box", "round": 0.02, "detail": 2, "x": x, "y": y, "z": z, "scale": 1, "sx": sx, "sy": sy, "sz": sz, **kw}


def ball(x, y, z, r, detail=10, **kw):
    return {"type": "mesh", "shape": "sphere", "detail": detail, "x": x, "y": y, "z": z, "scale": r, **kw}


def lamp(x=-3, y=5, z=-6, power=1.6, color="#fff4e6", reach=40):
    return {"type": "light", "x": x, "y": y, "z": z, "power": power, "reach": reach, "color": color}


def post3d(x=-3, y=5, z=-6, shadow=0.7, ao=0.5, thr=0.9, glow=0.3, size=1024):
    """The finish of a lit 3D scene: shadows from the lamp at x, y, z, creases, tone, edges."""
    return [{"type": "shadowmap", "amount": shadow, "soft": 2.5, "size": size, "sun": 0, "x": x, "y": y, "z": z},
            {"type": "ao", "amount": ao, "radius": 0.06}, {"type": "tonemap", "knee": 0.7}, {"type": "aa"},
            {"type": "bloom", "threshold": thr, "amount": f"{glow} + {glow}*audio.low", "radius": 0.014}]


def floor(c, y=0, color=None, rough=0.9, size=40):
    return {"type": "mesh", "shape": "plane", "detail": 4, "x": 0, "y": y, "z": 0, "scale": size, "material": "pbr", "rough": rough, "metal": 0, "color": color or "#2a2a2c", "rim": 0, "cull": True}


def now16(c):
    """Sixteenths since the scene began."""
    return f"(time.beat*4 - {c.a16:g})"


# ───────────────────────── probes (not dealt) ─────────────────────────

def probe(c):
    """Which way the shapes lie: a plane, a box, a torus and a cylinder, painted by vtx."""
    L = [lamp(),
         {"type": "mesh", "shape": "plane", "detail": 8, "x": -3, "y": -1, "z": 0, "scale": 1, "color": "#404040", "rim": 0, "paint_fine": True, "paint_color": "#ff4040", "paint": "step(0.8, vtx.x) + 0.5*step(0.8, vtx.z)"},
         box(-1, 0, 0, 0.5, 1.0, 0.2, color="#404040", rim=0, paint_fine=True, paint_color="#40ff40", paint="step(0.8, vtx.x) + 0.5*step(0.8, vtx.y)"),
         {"type": "mesh", "shape": "torus", "detail": 24, "x": 1, "y": 0, "z": 0, "scale": 0.8, "tube": 0.1, "color": "#a0a0a0", "rim": 0},
         {"type": "mesh", "shape": "cylinder", "detail": 16, "x": 3, "y": 0, "z": 0, "scale": 1, "sx": 0.3, "sy": 1.0, "sz": 0.3, "color": "#a0a0ff", "rim": 0},
         {"type": "mesh", "shape": "cone", "detail": 16, "x": 3, "y": -1.6, "z": 0, "scale": 0.5, "color": "#ffa0a0", "rim": 0},
         {"type": "shape", "sides": 4, "radius": 0.1, "width": 0, "fill": 1, "x": 1.0, "y": 0.5, "color": "#ffff00"}]
    return {"background": "#101014", "camera": cam(0, 2, -9, zoom=1.6), "layers": L, "filters": []}


# ───────────────────────── lattices: a note is a thing ─────────────────────────

@idiom(needs=1, fam="lattice", paper=True)
def loom(c):
    """The bar is a loom sixteen threads wide; each note is a stitch, each bar a row. A riff
    of five walks across the cloth on the diagonal; common time stands in columns."""
    rows = 9
    w = 3.0 / 16
    L = [{"type": "shape", "sides": 4, "rotate": 0.125, "radius": 0.006, "width": 0, "fill": 1, "color": c.dim, "opacity": 0.5, "x": (k % 16 - 7.5) * w, "y": -0.82 + 0.19 * (k // 16)} for k in range(16 * rows)]
    for i, p in enumerate(c.riffs[:3]):
        shape = (4, 0, 3)[i]
        L.append({"type": "shape", "notes": {"track": p.name, "past": rows * 4}, "sides": shape, "rotate": 0.125 if shape == 4 else 0, "radius": f"{0.062 - 0.012*i:g}*(1 + 0.8*exp(0 - 3*note.age))", "width": 0,
                  "fill": "0.35 + 0.65*exp(0 - 0.5*note.age)", "color": c.col(i),
                  "x": f"({NOTE16} - 7.5)*{w:g}", "y": f"-0.82 + 0.19*(time.bar - {NBAR}) - 0.19*smooth(0, 1, fract(time.bar))*0"})
    # The reed: where the cloth is being made.
    L.append({"type": "shape", "sides": 4, "rotate": 0.125, "radius": 0.012, "width": 0, "fill": 1, "color": c.dim, "count": 1,
              "x": f"(fract(time.bar)*16 - 7.5)*{w:g}", "y": -0.82})
    return {"background": c.bg, "layers": L, "filters": [bloom(c, 0.15, 0.012, 0.8)]}


@idiom(needs=2, fam="lattice", paper=True)
def remainder(c):
    """A board as wide as one riff and as tall as another. A lamp crosses it on the diagonal,
    a square a sixteenth, going off one edge and coming on at the other: it visits every
    square once before it is back where it began, and that is the long wait."""
    A, B = c.riffs[0], c.riffs[1]
    a, b = A.cell, B.cell
    L = math.lcm(a, b)
    u = min(7.6 / a, 4.2 / b)
    now = f"(time.beat*4 - {A.anchor:g})"
    off = (B.anchor - A.anchor) % b
    # Step s of the round stands at (s mod a, (s - off) mod b).
    x = f"(floor(fract((inst.i + 0.5)/{a})*{a}) - {(a - 1) / 2:g})*{u:g}"
    y = f"(floor(fract((inst.i - {off} + {b * 64} + 0.5)/{b})*{b}) - {(b - 1) / 2:g})*{u:g}"
    age = f"fract(({now} - inst.i)/{L})*{L}"       # sixteenths since the lamp was here
    lit = f"(0.05 + 0.95*exp(0 - 5*{age}/{L}))"
    layers = [box(x, y, 0, 0.42 * u, 0.42 * u, 0.02, count=L, **glow(c.ink, f"0.9*{lit}"), opacity=1)]
    # Each riff's own first square, in its colour: a column and a row.
    for P, col in ((A, c.a), (B, c.b)):
        k = L // P.cell
        o = (P.anchor - A.anchor) % P.cell
        xi = x.replace("inst.i", f"(inst.i*{P.cell} + {o})")
        yi = y.replace("inst.i", f"(inst.i*{P.cell} + {o})")
        ag = age.replace("inst.i", f"(inst.i*{P.cell} + {o})")
        layers.append(box(xi, yi, -0.05, 0.3 * u, 0.3 * u, 0.02, count=k, **glow(col, f"0.25 + 1.4*exp(0 - 4*{ag}/{L}) + 0.6*{P.hit}")))
    # The lamp itself.
    s = f"floor({now} + 0.001)"
    layers.append(box(x.replace("inst.i", s), y.replace("inst.i", s), -0.1, 0.47 * u, 0.47 * u, 0.03, **glow(c.c, f"1.6 + 1.5*{A.hit}")))
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.35, 0.018)]}


@idiom(needs=3, fam="lattice", cost=2)
def crystal(c):
    """Three riffs make a block of points, one riff along each edge; the lamp goes through it
    on the long diagonal and comes round only when all three have."""
    P = c.riffs[:3]
    cells = [p.cell for p in P]
    L = math.lcm(*cells)
    if L > 2400:
        P, cells = P[:2] + [P[2]], cells
    u = 4.5 / max(cells)
    now = f"(time.beat*4 - {P[0].anchor:g})"

    def co(k, i="inst.i"):
        n_, off = cells[k], (P[k].anchor - P[0].anchor) % cells[k]
        return f"(floor(fract(({i} - {off} + {n_ * 64} + 0.5)/{n_})*{n_}) - {(n_ - 1) / 2:g})*{u:g}"
    age = f"fract(({now} - inst.i)/{L})*{L}"
    count = min(L, 4000)
    layers = [ball(co(0), co(1), co(2), f"{0.14 * u:g}*(1 + 2.2*exp(0 - 9*{age}/{L}))", detail=6, count=count, **glow(c.ink, f"0.3 + 2.2*exp(0 - 7*{age}/{L})"))]
    n1, n2, n3 = cells
    if L < n1 * n2 * n3 <= 4096:
        # The lengths share a measure, so the lamp never visits most of the block: show it all, faintly.
        g = [f"(fract((inst.i + 0.5)/{n1})*{n1} - 0.5 - {(n1 - 1) / 2:g})*{u:g}", f"(fract((floor(inst.i/{n1}) + 0.5)/{n2})*{n2} - 0.5 - {(n2 - 1) / 2:g})*{u:g}",
             f"(floor(inst.i/{n1 * n2}) - {(n3 - 1) / 2:g})*{u:g}"]
        layers.insert(0, ball(g[0], g[1], g[2], 0.07 * u, detail=4, count=n1 * n2 * n3, **glow(c.dim, 0.5)))
    s = f"floor({now} + 0.001)"
    layers.append(ball(co(0, s), co(1, s), co(2, s), 0.42 * u, detail=10, **glow(c.a, 3)))
    spin = f"time.bar/{max(8, int(c.bars * 2))}"
    return {"background": c.bg, "camera": cam(f"7.5*sin({spin})", "2.2 + 1.2*sin(time.bar/11)", f"0 - 7.5*cos({spin})", zoom=2.3),
            "layers": layers, "filters": [bloom(c, 0.5, 0.02, 0.5)]}


@idiom(needs=1, fam="lattice", cost=2)
def helix(c):
    """The notes are beads let down a column that is as far round as the riff is long. What
    repeats with the riff hangs in straight files; common time goes round it like a thread.
    Half way through, the column is recut to the bar, and the files and threads change places."""
    parts = (c.riffs + c.drums)[:4]
    A = c.riffs[0]
    wide = f"mix({A.cell}, 16, smooth(0.42, 0.58, {c.prog}))" if c.variant % 2 == 0 else f"mix(16, {A.cell}, smooth(0.42, 0.58, {c.prog}))"
    layers = []
    for i, p in enumerate(parts):
        th = f"(0.25 - div(note.age*4, {wide}))"
        r = 1.5 + 0.22 * i
        layers.append(ball(f"{r}*cos({th})", "2.6 - 0.16*note.age", f"{r}*sin({th})", f"{0.115 - 0.015 * i:g}*(1 + 1.5*exp(0 - 4*note.age))", detail=8,
                           notes={"track": p.name, "past": 34}, **glow(c.col(i), "0.75 + 2.8*exp(0 - 2*note.age)")))
    # The column's hoops, a bar apart.
    layers.append({"type": "mesh", "shape": "torus", "detail": 40, "count": 8, "x": 0, "y": "2.6 - 0.64*(inst.i + fract(time.bar))", "z": 0, "scale": 1.75, "tube": 0.012, **glow(c.dim, 0.85)})
    return {"background": c.bg, "camera": cam("5.6*sin(time.bar/24)", 1.9, "0 - 5.6*cos(time.bar/24)", look=(0, 0.3, 0), zoom=1.35), "layers": layers, "filters": [bloom(c, 0.45, 0.02, 0.5)]}


@idiom(needs=1, fam="lattice", paper=True)
def spiral(c):
    """A disc that turns once a riff: every note is set down at the centre and carried
    outward. The riff's own notes stand in spokes; everything else winds."""
    parts = (c.riffs + c.drums)[:4]
    wide = c.riffs[0].cell if c.variant % 2 == 0 else 16
    layers = []
    for i, p in enumerate(parts):
        th = f"(0.25 - note.age*4/{wide})"
        r = "(0.08 + 0.045*note.age)"
        layers.append({"type": "shape", "notes": {"track": p.name, "past": 20}, "sides": 1, "radius": f"{0.05 - 0.006 * i:g}*(0.6 + note.vel)*(1 + 1.2*exp(0 - 4*note.age))", "width": 0, "fill": 1,
                       "color": c.col(i), "x": f"{r}*cos({th})", "y": f"{r}*sin({th})"})
    layers.append({"type": "shape", "sides": 0, "radius": 0.97, "width": 0.008, "fill": 0, "color": c.dim})
    return {"background": c.bg, "layers": layers, "filters": [bloom(c, 0.15, 0.012, 0.8)]}


@idiom(needs=1, fam="fall", cost=2)
def dominoes(c):
    """A row of dominoes for each part, stood as far apart as its notes are; each comes down
    on its note."""
    parts = (c.riffs + c.drums)[:3]
    layers = [lamp(-2, 6, -5, 1.7), floor(c, 0, "#26262a", 0.85)]
    for i, p in enumerate(parts):
        z = 1.1 * i - 0.6
        fall = "0.21*smooth(-0.5, 0, note.age)"
        h = 0.5
        layers.append(box(f"0 - 1.3*note.age - {h}*sin({fall})", f"{h}*cos({fall}) + 0.03", z, 0.05, h, 0.22, rz=fall, notes={"track": p.name, "past": 10, "ahead": 12},
                          **solid(c.col(i), 0.45), emit="0.6*exp(0 - 3*max(note.age, 0))*step(0, note.age)"))
    look = {"background": c.bg, "layers": layers, "filters": post3d(-2, 6, -5)}
    return shots(c, look, [cam("2.4 + 0.8*sin(time.bar/13)", 1.1, -4.2, look=(0.2, 0.3, 0.4), zoom=1.25), cam(6.5, 0.9, 0.3, look=(0, 0.3, 0.3), zoom=1.5), cam(1.0, 6.0, -1.0, look=(1.0, 0, 0.4), zoom=1.3)])


@idiom(needs=2, fam="orbit", cost=2)
def orrery(c):
    """A sun and a planet for each riff, its year the riff's length. They stand in line only
    where the riffs come round together."""
    parts = c.riffs[:4]
    layers = [{"type": "stars", "count": 500, "speed": 0, "size": 0.8, "light": 0.5, "twinkle": 0.2, "streak": 0},
              lamp(0, 0.2, 0, 2.2, "#fff0d8", 30), ball(0, 0, 0, 0.42, 16, **glow("#ffe9c0", 2.2))]
    for i, p in enumerate(parts):
        r = 1.25 + 0.85 * i
        th = f"(0.25 - {p.turn})"
        layers.append({"type": "trail", "x": f"{r}*cos({th})", "y": 0, "z": f"{r}*sin({th})", "length": f"{p.cell * 0.9}*0.125/time.bpm", "samples": 90, "width": 0.03, "taper": 0.6, "glow": 0.8, "fade": 1, "color": c.col(i)})
        layers.append(ball(f"{r}*cos({th})", 0, f"{r}*sin({th})", f"{0.2 + 0.05 * i:g}*(1 + 0.5*{p.hit})", 14, **solid(c.col(i), 0.6), emit=f"0.3 + 0.9*{p.hit}"))
        layers.append({"type": "mesh", "shape": "torus", "detail": 64, "x": 0, "y": 0, "z": 0, "scale": r / 0.8, "tube": 0.006, **glow(c.dim, 0.5)})
    # The line they stand in.
    layers.append({"type": "beam", "from": [0, 0, 0], "to": [0, 0, 1.25 + 0.85 * len(parts)], "width": 0.006, "glow": 0.35, "color": c.dim})
    return {"background": "#020204", "camera": [cam("0.8*sin(time.bar/17)", 3.4, -5.4, look=(0, 0, 0.4), zoom=1.45), cam(0.01, 8.5, -0.2, look=(0, 0, 0), zoom=1.75), cam(0, 0.5, -7.5, look=(0, 0, 0), zoom=1.7)][c.variant % 3],
            "layers": layers, "filters": [bloom(c, 0.5, 0.02, 0.6), {"type": "aa"}]}


@idiom(needs=0, fam="swing", cost=2)
def pendwave(c):
    """Fifteen pendulums, each a little quicker than the last. They start together, fall out
    into waves and files, and are together again exactly as the scene ends."""
    N = 15
    n0 = max(20, round((c.b16 - c.a16) / 5))
    tau = c.prog
    layers = [lamp(-3, 6, -6, 1.7), floor(c, -2.3, "#1d1d20", 0.7)]
    z = f"(inst.i - {(N - 1) / 2})*0.42"
    Lk = f"(3.4*pow({n0}/({n0} + inst.i), 2))"
    th = f"(0.075*cos(({n0} + inst.i)*{tau}))"
    bx, by = f"{Lk}*sin({th})", f"2.0 - {Lk}*cos({th})"
    layers.append({"type": "beam", "count": N, "from": [0, 2.0, z], "to": [bx, by, z], "width": 0.006, "glow": 0.5, "color": c.dim})
    layers.append(ball(bx, by, z, 0.16, 14, count=N, **solid(c.ink, 0.25, 0.9), emit=f"0.25 + 0.5*track.*.hit"))
    layers.append(box(0, 2.03, 0, 0.05, 0.03, N * 0.21 + 0.2, **solid(c.dim, 0.6)))
    front = c.variant % 2 == 0
    camera = cam(0.3, 0.4, -9.5, look=(0, -0.4, 0), zoom=1.6) if front else cam(-2.5, 5.5, -7.5, look=(0, -0.9, 0), zoom=1.7)
    return {"background": c.bg, "camera": camera, "layers": layers, "filters": post3d(-3, 6, -6)}


@idiom(needs=2, fam="field", paper=True)
def moire(c):
    """Two sets of rings, as many to the unit as each riff has sixteenths, laid over one
    another: where they agree the picture is quiet, and the fringes between go by at the
    difference of the two."""
    A, B = c.riffs[0], c.riffs[1]
    layers = [
        {"type": "rings", "count": A.cell * 1.3, "speed": 0, "duty": 0.5, "soft": 0.02, "x": f"0.5*cos({A.turn}/2)", "y": f"0.28*sin({A.turn}/2)", "color": "#ffffff", "spread": 0},
        {"type": "rings", "count": B.cell * 1.3, "speed": 0, "duty": 0.5, "soft": 0.02, "x": f"0 - 0.5*cos({B.turn}/2)", "y": f"0 - 0.28*sin({B.turn}/2)", "color": "#ffffff", "spread": 0, "blend": "difference"},
    ]
    return {"background": "#000000", "layers": layers, "filters": [{"type": "tint", "palette": [c.bg, c.a, c.ink], "amount": 1, "pos": 0}, bloom(c, 0.25)]}


@idiom(needs=1, fam="thread", paper=True)
def stringart(c):
    """Pins round a circle, a thread from each to the pin so many times further on. The
    multiplier goes up one for every turn of the riff, and the figure folds again."""
    A = c.riffs[0]
    N = A.cell * (16 if A.cell <= 7 else 10)
    T = f"({now16(c)}/{A.cell} + 2)"
    m = f"(floor({T}) + smooth(0.55, 1, fract({T})))"
    R = 2.3
    layers = [{"type": "beam", "count": N, "from": [f"{R}*cos(inst.i/{N} + 0.25)", f"{R}*sin(inst.i/{N} + 0.25)", 0], "to": [f"{R}*cos(inst.i*{m}/{N} + 0.25)", f"{R}*sin(inst.i*{m}/{N} + 0.25)", 0],
               "width": 0.006, "glow": f"0.35 + 0.5*{A.hit}", "color": c.ink, "samples": 24}]
    if len(c.riffs) > 1:
        B = c.riffs[1]
        layers.append(ball(f"{R}*cos(0.25 - {B.turn})", f"{R}*sin(0.25 - {B.turn})", -0.1, 0.09, 10, **glow(c.a, 3)))
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.4, 0.016, 0.5)]}


@idiom(needs=1, fam="mirror")
def mandala(c):
    """A few plain shapes moved by the riffs, seen in a kaleidoscope of as many mirrors as the
    riff has sixteenths: a five makes fivefold figures, a seven sevenfold."""
    parts = c.riffs[:3]
    A = parts[0]

    def fold(n_):       # no more mirrors than leave a wedge wide enough to hold anything
        while n_ > 12:
            n_ = next((n_ // k for k in (2, 3, 5, 7) if n_ % k == 0), 7)
        return max(n_, 3)
    folds = [fold(p.cell) for p in parts[:2]]
    nn = folds[0] if len(folds) < 2 else f"mix({folds[0]}, {folds[1]}, step(0.5, fract(time.bar/4)))"
    # The mirrors show the wedge that begins at `rot` and is half a fold wide: everything is
    # kept inside it, and goes round with it.
    rot = f"({A.turn}/{A.cell * 4})"
    wedge = 0.5 / max(folds)
    layers = []
    for i, p in enumerate(parts):
        th = f"({rot} + {wedge:.4f}*(0.5 + 0.4*sin({p.turn} + {i / 3:.3f})))"
        r = f"(0.2 + 0.5*(0.5 + 0.5*sin({p.turn}*2 + {i / 4:.3f})))"
        layers.append({"type": "shape", "sides": (3, 4, 5)[i], "radius": f"0.2 + 0.1*{p.hit}", "width": 0.012, "fill": f"0.25 + 0.6*{p.hit}", "color": c.col(i), "x": f"{r}*cos({th})", "y": f"{r}*sin({th})", "rotate": p.turn})
        tn = f"({rot} + {wedge:.4f}*(0.1 + 0.8*{p.nph}))"
        layers.append({"type": "shape", "notes": {"track": p.name, "past": 6}, "sides": 1, "radius": "0.03*(1 + exp(0 - 3*note.age))", "width": 0, "fill": 1, "color": c.col(i + 1),
                       "x": f"(0.08 + 0.16*note.age)*cos({tn})", "y": f"(0.08 + 0.16*note.age)*sin({tn})"})
    return {"background": c.bg, "layers": layers, "filters": [{"type": "kaleido", "n": nn, "rotate": rot, "zoom": 1.0}, bloom(c, 0.35)]}


@idiom(needs=2, fam="field", paper=True, cost=2)
def chladni(c):
    """A plate with sand on it, sounded: the sand lies along the lines that stand still, and
    there are as many of them each way as the two riffs are long."""
    A, B = c.riffs[0], c.riffs[1]
    a, b = A.cell, B.cell
    while a > 9:
        a = (a + 1) // 2
    while b > 9:
        b = (b + 1) // 2
    if a == b:
        b += 1
    # (x, y run -1..1 over the plate; cos takes turns, so n/4 turns to the unit is n half waves.)
    f = lambda n_, m_: f"(cos({n_ / 4:g}*vtx.x)*cos({m_ / 4:g}*vtx.y) - cos({m_ / 4:g}*vtx.x)*cos({n_ / 4:g}*vtx.y))"  # noqa: E731
    mixv = f"smooth(0.3, 0.7, tri(time.bar/4)*0.5 + 0.5)"
    a2, b2 = (a + 1, b + 2) if a + 1 != b + 2 else (a + 2, b + 1)      # (equal numbers each way would be no figure at all)
    field = f"abs(mix({f(a, b)}, {f(a2, b2)}, {mixv}))"
    sand = f"(1 - smooth(0.0, 0.1 + 0.25*{A.hit}, {field}))"
    plate = box(0, 0, 0, 2.2, 2.2, 0.02, color="#0b0b0d", light=0.2, ambient=0.6, rim=0, paint_fine=True, paint_color=c.ink, paint=sand)
    return {"background": c.bg, "camera": cam(0, 0, -9, zoom=2.3, roll=f"0.01*sin(time.bar/8)"), "layers": [plate], "filters": [bloom(c, 0.3, 0.012)]}


@idiom(needs=0, fam="orbit")
def eclipse(c):
    """A sun, and a moon for each riff going over it once a turn. All of them cover it at once
    only where the riffs meet."""
    parts = c.riffs[:3] or _cast(c, 1)
    if not parts:
        raise ValueError("no one to be a moon")
    cover = " * ".join(f"smooth(0.2, 0.02, abs(fract({p.turn} + 0.5) - 0.5))" for p in parts)
    layers = [{"type": "stars", "count": 400, "speed": 0, "size": 0.9, "light": f"0.25 + 1.5*({cover})", "twinkle": 0.3, "streak": 0},
              {"type": "shape", "sides": 1, "radius": 0.34, "width": 0, "fill": 1, "color": "#fff3d4", "glow": f"0.25 + 0.9*({cover})"}]
    for i, p in enumerate(parts):
        x = f"{1.5 + 0.25 * i}*tri({p.turn} + 0.25)"
        layers.append({"type": "shape", "sides": 1, "radius": 0.345 - 0.03 * i, "width": 0, "fill": 1, "color": "#000000", "x": x, "y": f"{0.05 * (i - 1)}*cos({p.turn})"})
        layers.append({"type": "shape", "sides": 0, "radius": 0.345 - 0.03 * i, "width": 0.004, "fill": 0, "color": c.col(i), "x": x, "y": f"{0.05 * (i - 1)}*cos({p.turn})", "opacity": 0.8})
    return {"background": "#010103", "layers": layers, "filters": [bloom(c, 0.3, 0.03, 0.7)]}


def probe2(c):
    """What a pose's three numbers do to an arm and a leg."""
    L = [lamp(-3, 5, -6), floor(c, 0, "#303034")]
    poses = [{}, {"arm_l": [0.2, 0, 0]}, {"arm_l": [0, 0.2, 0]}, {"arm_l": [0, 0, 0.2]}, {"arm_r": [0.2, 0, 0], "forearm_r": [0.2, 0, 0]}, {"thigh_l": [0.2, 0, 0], "shin_l": [0.2, 0, 0]},
             {"arm_l": [-0.2, 0, 0], "arm_r": [0, 0, -0.2]}, {"spine": [0.1, 0, 0], "head": [0, 0.2, 0]}]
    for i, p in enumerate(poses):
        L.append({"type": "figure", "rig": "human", "motion": "none", "pose": p, "x": (i - 3.5) * 1.1, "y": 1.05, "z": 0, "scale": 1, "color": "#d8d0c0", "material": "pbr", "rough": 0.8, "melt": 0.05, "rim": 0})
    return {"background": "#101014", "camera": cam(0, 1.4, -8, look=(0, 1, 0), zoom=1.5), "layers": L, "filters": []}


# ───────────────────────── bodies ─────────────────────────

def skin(color, emit=0.0):
    return {"color": color, "material": "pbr", "rough": 0.8, "metal": 0, "melt": 0.05, "rim": 0, "emit": emit}


def hit_env(parts, decay="260ms"):
    """An envelope for each part's notes: env.h0, env.h1, …"""
    return {f"h{i}": {"on": f"track.{p.name}", "attack": "0ms", "decay": decay} for i, p in enumerate(parts)}


@idiom(needs=0, fam="body", cost=3)
def puppet(c):
    """One body, each limb on a string, each string pulled by a different part: the right
    arm keeps one riff's time and the left another's, the legs the drums'."""
    drivers = (c.riffs + c.drums + c.tunes + c.parts)[:5]
    seen, drv = set(), []
    for p in drivers:
        if p.name not in seen:
            seen.add(p.name), drv.append(p)
    env = hit_env(drv)
    e = lambda i: f"env.h{i}" if i < len(drv) else "0"  # noqa: E731
    pose = {
        "arm_r": [f"0.03 + 0.24*{e(0)}", 0, f"0.05 + 0.1*{e(0)}"], "forearm_r": [f"0.08 + 0.2*{e(0)}", 0, 0],
        "arm_l": [f"0.03 + 0.24*{e(1)}", 0, f"0 - 0.05 - 0.1*{e(1)}"], "forearm_l": [f"0.08 + 0.2*{e(1)}", 0, 0],
        "thigh_l": [f"0.2*{e(2)}", 0, -0.01], "shin_l": [f"0 - 0.22*{e(2)}", 0, 0],
        "thigh_r": [f"0.2*{e(3)}", 0, 0.01], "shin_r": [f"0 - 0.22*{e(3)}", 0, 0],
        "head": [f"0.05*{e(4)}", f"0.04*sin(time.bar/2)", 0], "spine": [0.01, "0.02*sin(time.bar/4)", 0],
    }
    S = 1.7
    layers = [lamp(-2.5, 6, -5, 0.7), lamp(3, 3, -4, 0.5, c.a), floor(c, 0, "#1c1c20", 0.8),
              {"type": "figure", "rig": "human", "motion": "none", "name": "pup", "pose": pose, "x": 0, "y": f"{1.05 * S:g} + 0.04*{e(2)} + 0.04*{e(3)}", "z": 0, "scale": S, **skin("#d9d2c4", 0.05)},
              box(0, 4.6, 0, 1.3, 0.04, 0.04, **solid(c.dim))]
    for i, (bone, bx) in enumerate((("forearm_r", 1.1), ("forearm_l", -1.1), ("shin_l", -0.5), ("shin_r", 0.5), ("head", 0.0))):
        if i < len(drv):
            layers.append({"type": "beam", "from": [bx, 4.6, 0], "to": [f"actor.pup.{bone}.x", f"actor.pup.{bone}.y", f"actor.pup.{bone}.z"], "width": 0.008, "glow": f"0.3 + 1.6*{e(i)}", "color": c.col(i)})
    look = {"background": c.bg, "env": env, "layers": layers, "filters": post3d(-2.5, 6, -5)}
    return shots(c, look, [cam("0.9*sin(time.bar/9)", 2.0, -6.3, look=(0, 2.25, 0), zoom=2.3), cam(-2.6, 3.4, -3.6, look=(0, 2.6, 0), zoom=1.9), cam(2.2, 0.5, -4.4, look=(0, 1.7, 0), zoom=1.6)], drv[0])


@idiom(needs=1, fam="body", cost=3, max_cell=12)
def chorus(c):
    """A line of as many dancers as the riff has sixteenths; the move goes down the line once
    a turn. A second line behind keeps another riff."""
    layers = [lamp(-3, 6, -6, 0.7), lamp(4, 4, -5, 0.5, c.b), floor(c, 0, "#1e1e22", 0.7)]
    for i, p in enumerate(c.riffs[:2]):
        nn = min(p.cell, 12)
        d = f"(fract({p.turn} - inst.i/{nn})*{nn})"       # sixteenths since this dancer's step
        e = f"exp(0 - 0.9*{d})"
        S = 1.0 - 0.1 * i
        layers.append({"type": "figure", "rig": "human", "motion": "none", "count": nn, "x": f"(inst.i - {(nn - 1) / 2})*{min(0.95, 7.5 / nn):g}", "y": f"{1.05 * S:g} + 0.12*{e}", "z": 1.6 * i, "scale": S,
                       "pose": {"arm_l": [f"0.1*{e}", 0, f"0 - 0.36*{e}"], "arm_r": [f"0.1*{e}", 0, f"0.36*{e}"], "thigh_l": [f"0.06*{e}", 0, 0], "shin_l": [f"0 - 0.1*{e}", 0, 0], "head": [f"0 - 0.04*{e}", 0, 0]},
                       **skin("#b9b3a8", f"0.9*{e}"), "color": c.col(i) if i else "#b9b3a8"})
    look = {"background": c.bg, "layers": layers, "filters": post3d(-3, 6, -6)}
    return shots(c, look, [cam("1.5*sin(time.bar/11)", 1.5, -7.2, look=(0, 1.0, 0.6), zoom=2.6), cam(-6.5, 1.3, -1.2, look=(0, 1.1, 0.6), zoom=1.7), cam(0, 6.5, -3.5, look=(0, 0.9, 0.6), zoom=2.0)])


@idiom(needs=1, fam="body", cost=2)
def semaphore(c):
    """Signallers on a ridge at dusk: each keeps a part, and moves an arm on to the next
    station with every sixteenth of its riff."""
    parts = (c.riffs + c.drums)[:3]
    layers = [{"type": "gradient", "palette": [c.b, c.a, "#1a0f1e", "#050308"], "angle": 0.25, "spread": 0.9, "res": 0.5},
              {"type": "shape", "sides": 1, "radius": 0.2, "width": 0, "fill": 1, "color": "#fff0c8", "x": -0.9, "y": -0.28},
              box(0, -2.2, 0.5, 9, 1.0, 0.2, color="#030303", light=0, ambient=0, rim=0)]
    dark = {"color": "#030303", "light": 0, "ambient": 0, "rim": 0, "emit": 0}
    for i, p in enumerate(parts):
        k = f"floor({p.ph}*{p.cell} + 0.02)"
        a_r = f"(0.06 + 0.11*fract({k}/4)*4)"
        a_l = f"(0.06 + 0.11*floor(fract({k}/{max(p.cell, 2)})*4))"
        x = (i - (len(parts) - 1) / 2) * 2.6
        layers.append({"type": "figure", "rig": "human", "motion": "none", "x": x, "y": 0.05, "z": 0, "scale": 1.25, **dark,
                       "extra": [{"name": "flag_r", "parent": "forearm_r", "length": 0.42, "dir": [0, -1, 0], "width": 0.03}, {"name": "flag_l", "parent": "forearm_l", "length": 0.42, "dir": [0, -1, 0], "width": 0.03}],
                       "pose": {"arm_r": [0, 0, a_r], "arm_l": [0, 0, f"0 - {a_l}"]}})
    return {"background": "#050308", "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.3, 0.03, 0.7)]}


@idiom(needs=1, fam="body", cost=2)
def juggle(c):
    """Every note is thrown, and comes down exactly as the next one goes up: one juggler,
    as many patterns in the air as there are parts."""
    parts = c.riffs[:3]
    env = hit_env(parts)
    S = 1.5
    layers = [lamp(-2, 6, -5, 0.65), lamp(0, 0.4, -2, 0.5, c.a, 8), floor(c, 0, "#19191d", 0.8),
              {"type": "figure", "rig": "human", "motion": "none", "x": 0, "y": 1.05 * S, "z": 0, "scale": S, **skin("#d9d2c4", 0.03),
               "pose": {"arm_r": ["0.1 + 0.05*env.h0", 0, 0.03], "forearm_r": ["0.15 + 0.1*env.h0", 0, 0], "arm_l": [f"0.1 + 0.05*env.h{min(1, len(parts) - 1)}", 0, -0.03],
                        "forearm_l": [f"0.15 + 0.1*env.h{min(1, len(parts) - 1)}", 0, 0], "head": ["0 - 0.05", 0, 0]}}]
    for i, p in enumerate(parts):
        gap = "max(note.gap, 0.24)"
        u = f"clamp(div(note.age, {gap}), 0, 1)"
        side = f"(1 - 2*step(0.5, fract({p.nstep}/2 + 0.01)))"
        w = 0.42 + 0.22 * i
        layers.append(ball(f"{side}*{w}*(1 - 2*{u})", f"{1.02 * S:g} + (0.5 + 1.5*{gap})*4*{u}*(1 - {u})", f"-0.45 - {0.05 * i}", f"0.085*step(note.age, {gap})", 10,
                           notes={"track": p.name, "past": 8}, **solid(c.col(i), 0.4), emit=0.6))
    look = {"background": c.bg, "env": env, "layers": layers, "filters": post3d(-2, 6, -5)}
    return shots(c, look, [cam("0.5*sin(time.bar/7)", 2.3, -6.0, look=(0, 2.3, 0), zoom=2.2), cam(3.0, 3.6, -3.6, look=(0, 2.5, -0.3), zoom=1.7), cam(-3.4, 2.6, -3.2, look=(0, 2.4, -0.3), zoom=1.8)])


@idiom(needs=2, fam="body", cost=3)
def maypole(c):
    """A pole, and a dancer for each part on a ribbon, going round once a riff, alternate ones
    the other way: they pass each other where the riffs cross."""
    parts = (c.riffs + c.drums)[:6]
    layers = [{"type": "sky", "zenith": "#3d6fb0", "horizon": "#cfe0ee", "ground": "#5d7a45", "sun": "#fff2d0", "sun_yaw": 0.62, "sun_height": 0.1, "clouds": 0.25},
              floor(c, 0, "#5f8246", 0.95), {"type": "mesh", "shape": "cylinder", "detail": 12, "x": 0, "y": 1.9, "z": 0, "scale": 1, "sx": 0.05, "sy": 1.9, "sz": 0.05, **solid("#e8e2d2", 0.6)},
              ball(0, 3.85, 0, 0.1, 10, **solid(c.a, 0.4, 0.6))]
    for i, p in enumerate(parts):
        r = 1.7 + 0.28 * (i % 2)
        th = f"({'0 - ' if i % 2 else ''}{p.turn} + {i / len(parts):.3f})"
        x, z = f"{r}*cos({th})", f"{r}*sin({th})"
        layers.append({"type": "figure", "rig": "human", "motion": "walk", "phase": f"4*{p.turn} - time.beat", "x": x, "y": 0.95, "z": z, "scale": 0.9,
                       "ry": f"{th} + {0.5 if i % 2 else 0}", **skin(c.col(i), 0.0), "pose": {"arm_r": [0, 0, 0.33], "forearm_r": [0, 0, 0.05]}})
        layers.append({"type": "beam", "from": [0, 3.8, 0], "to": [x, 1.85, z], "width": 0.03, "glow": 0.9, "sag": 0.12, "color": c.col(i)})
    spin = "time.bar/40"
    return {"background": "#cfe0ee", "camera": [cam(f"7*sin({spin})", 3.3, f"0 - 7*cos({spin})", look=(0, 1.6, 0), zoom=1.35), cam(0.01, 9.5, -0.6, look=(0, 0, 0), zoom=1.5)][c.variant % 2], "layers": layers,
            "filters": [{"type": "shadowmap", "amount": 0.6, "soft": 2, "size": 1024}, {"type": "ao", "amount": 0.5, "radius": 0.05}, {"type": "tonemap", "knee": 0.8}, {"type": "aa"}]}


# ───────────────────────── rooms and machines ─────────────────────────

@idiom(needs=1, fam="room", cost=3)
def doors(c):
    """A wall of doors with a bright room behind. Each door is on a part's hinge: it swings
    open and shut once a turn, and the light comes through in its time."""
    parts = (c.every + c.drums)[:7]
    names, P = set(), []
    for p in parts:
        if p.name not in names and p.cell:
            names.add(p.name), P.append(p)
    P = P[:6] or c.riffs[:1]
    nn = len(P)
    sp, w, h = 1.5, 0.5, 1.15
    layers = [lamp(0, 3.0, 4.5, 2.6, "#ffe6b8", 16), lamp(-2, 5, -6, 0.7),
              floor(c, 0, "#22222a", 0.35), box(0, h, 5.5, 12, h + 0.6, 0.1, **glow("#ffdca0", 1.4))]
    # The wall: piers between the doorways and a lintel over them.
    layers.append(box(f"(inst.i - {nn / 2})*{sp}", h, 1.0, (sp - 2 * w) / 2, h, 0.08, count=nn + 1, **solid("#2a2a30", 0.8)))
    layers.append(box(0, 2 * h + 0.6, 1.0, nn * sp / 2 + 0.3, 0.6, 0.08, **solid("#2a2a30", 0.8)))
    for side in (-1, 1):
        layers.append(box(side * (nn * sp / 2 + 6.2), h, 1.0, 6, h + 1, 0.08, **solid("#2a2a30", 0.8)))
    for i, p in enumerate(P):
        a = f"(0.22*(0.5 - 0.5*cos({p.turn})))"
        hx = (i - (nn - 1) / 2) * sp - w
        layers.append(box(f"{hx:g} + {w}*cos({a})", h, f"0.98 - {w}*sin({a})", w, h, 0.03, ry=a, **solid(c.col(i), 0.55), emit=f"0.25*{p.hit}"))
    return {"background": "#060608", "camera": cam("1.2*sin(time.bar/10)", 1.25, -6.4, look=(0, 1.1, 1), zoom=1.3), "layers": layers,
            "filters": [{"type": "shadowmap", "amount": 0.8, "soft": 2.5, "size": 1024, "sun": 0, "x": 0, "y": 3.0, "z": 4.5}, {"type": "ao", "amount": 0.5, "radius": 0.06},
                        {"type": "rays", "x": 0, "y": 1.3, "z": 5, "amount": 0.5, "length": 0.6, "threshold": 0.7}, {"type": "tonemap", "knee": 0.7}, {"type": "aa"}, bloom(c, 0.3, 0.02, 0.8)]}


@idiom(needs=1, fam="room", paper=True)
def blinds(c):
    """A blind of slats before a lit window: a wave goes down it as long as the riff, and
    another across it for the second."""
    A = c.riffs[0]
    N = 26
    layers = [box(0, 0, 0.6, 5, 3, 0.02, **glow(c.a, 1.1))]
    a = f"(0.25*smooth(0.25, 0.75, 0.5 + 0.5*sin({A.turn} - inst.i/{A.cell})))"
    layers.append(box(0, f"(inst.i - {(N - 1) / 2})*0.2", 0, 4.7, 0.1, 0.008, count=N, rx=a, color=c.bg, light=0.5, ambient=0.2, rim=0))
    if len(c.riffs) > 1:
        B = c.riffs[1]
        M = 40
        b = f"(0.25*smooth(0.25, 0.75, 0.5 + 0.5*sin({B.turn} - inst.i/{B.cell})))"
        layers.append(box(f"(inst.i - {(M - 1) / 2})*0.24", 0, -0.4, 0.12, 2.7, 0.008, count=M, ry=b, color=c.bg, light=0.5, ambient=0.2, rim=0))
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.4, 0.03, 0.6)]}


@idiom(needs=1, fam="string", paper=True)
def strings(c):
    """A string for each part, standing in as many loops as its riff has sixteenths, and
    plucked by its notes."""
    names, P = set(), []
    for p in c.every + c.drums + c.tunes:
        if p.name not in names:
            names.add(p.name), P.append(p)
    P = P[:7]
    env = hit_env(P, "500ms")
    layers = []
    # Where there are few parts each has sympathetic strings as well, standing in twice and
    # three times as many loops and sounding more faintly.
    over = max(1, 5 // len(P))
    rows = [(i, p, h) for i, p in enumerate(P) for h in range(1, over + 1)]
    for r, (i, p, h) in enumerate(rows):
        y = ((len(rows) - 1) / 2 - r) * min(0.62, 4.2 / len(rows))
        layers.append({"type": "beam", "from": [-4.1, y, 0], "to": [4.1, y, 0], "samples": 220, "width": 0.045 / h ** 0.5, "glow": f"{0.8 / h:g} + {1.6 / h ** 0.5:g}*env.h{i}", "wave": f"{0.3 / h ** 0.5:g}*env.h{i}",
                       "waves": min((p.cell or 4) * h, 28), "speed": 3, "color": c.col(i) if h == 1 else c.col(i + h - 1)})
        for x in (-4.1, 4.1):
            layers.append(ball(x, y, 0, 0.05, 8, **glow(c.dim, 0.8)))
    return {"background": c.bg, "env": env, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.4, 0.02, 0.5)]}


@idiom(needs=1, fam="machine", cost=2)
def hammers(c):
    """A rank of hammers for each riff, one to a sixteenth of it that sounds; each lifts
    before its note and comes down on it."""
    parts = c.riffs[:3]
    layers = [lamp(-2, 5, -5, 1.5), lamp(3.5, 2.5, -3, 0.8, c.a), floor(c, -0.12, "#22222a", 0.6)]
    for i, p in enumerate(parts):
        nn = p.cell
        dx = min(0.42, 6.4 / nn)
        z0 = 1.5 * i
        x = f"({p.nstep} - {(nn - 1) / 2})*{dx:g}"
        a = f"(0.14*smooth(0 - {nn / 8:g}, -0.12, note.age)*step(note.age, 0) + 0.14*(1 - exp(0 - 2.5*max(note.age, 0)))*step(0, note.age))"
        ln = 0.55
        layers.append(box(x, f"0.12 + {ln}*sin({a})", f"{z0} + 0.9 - {ln}*cos({a})", 0.035, 0.03, ln, rx=f"0 - {a}", notes={"track": p.name, "past": nn / 8, "ahead": nn / 8}, **solid("#b9a27c", 0.7)))
        layers.append(box(x, f"0.1 + {2 * ln}*sin({a})", f"{z0} + 0.9 - {2 * ln}*cos({a})", 0.07, 0.09, 0.06, rx=f"0 - {a}", notes={"track": p.name, "past": nn / 8, "ahead": nn / 8}, **solid(c.col(i), 0.9)))
        # The bars they strike, one a sixteenth.
        d = f"(fract({p.turn} - inst.i/{nn})*{nn})"
        layers.append(box(f"(inst.i - {(nn - 1) / 2})*{dx:g}", -0.04, z0 - 0.2, dx * 0.42, 0.04, 0.3, count=nn, **solid("#9c8a5a", 0.3, 0.9), emit=f"0.9*exp(0 - 1.5*{d})*{p.hit}"))
    look = {"background": c.bg, "layers": layers, "filters": post3d(-2, 5, -5)}
    return shots(c, look, [cam("0.8*sin(time.bar/9)", 2.4, -3.6, look=(0, 0.15, 1.1), zoom=2.3), cam(-4.2, 0.6, 0.2, look=(0, 0.25, 0.6), zoom=2.0), cam(0, 5.5, 0.4, look=(0, 0, 0.5), zoom=2.4)])


@idiom(needs=1, fam="travel", cost=2)
def railway(c):
    """A night line. Sleepers are sixteenths; the posts on one side stand a riff apart, those
    on the other side another riff apart, and a gantry spans the track every bar. Two posts
    pass together only where the riffs meet."""
    day = c.variant % 2 == 1
    A = c.riffs[0]
    B = c.riffs[1] if len(c.riffs) > 1 else None
    u = 0.42            # a sixteenth of track
    far = 70

    def along(period, anchor, count):
        return f"(inst.i*{period * u:g} - fract((time.beat*4 - {anchor:g})/{period})*{period * u:g})", count
    z, k = along(1, 0, far)
    layers = [box(0, 0.02, z, 0.95, 0.03, 0.07, count=k, **solid("#3a3026", 0.9))]
    for sx in (-0.6, 0.6):
        layers.append(box(sx, 0.09, 14, 0.03, 0.04, 16, **solid("#8a8a90", 0.3, 0.9)))
    z, k = along(16, 0, 6)
    layers += [box(0, 3.1, z, 2.3, 0.07, 0.07, count=k, **solid("#3c3c44", 0.6)), box(-2.3, 1.55, z, 0.07, 1.55, 0.07, count=k, **solid("#3c3c44", 0.6)), box(2.3, 1.55, z, 0.07, 1.55, 0.07, count=k, **solid("#3c3c44", 0.6))]
    for side, p, col in ((-1, A, c.a), (1, B, c.b)):
        if p is None:
            continue
        z, k = along(p.cell, p.anchor, max(4, int(far / p.cell) + 1))
        layers.append(box(side * 1.5, 0.9, z, 0.04, 0.9, 0.04, count=k, **solid("#55555c", 0.5)))
        layers.append(ball(side * 1.5, 1.9, z, 0.12, 8, count=k, **glow(col, f"1.4 + 2*{p.hit}")))
    if day:
        sky = {"type": "sky", "zenith": "#31527f", "horizon": "#e9c9a0", "ground": "#3d3a34", "sun": "#ffe2b0", "sun_yaw": 0.2, "sun_height": 0.04, "clouds": 0.3}
        return {"background": "#e9c9a0", "camera": cam(0, 1.25, -1.0, look=(0, 1.0, 8), zoom=1.0), "layers": [sky, floor(c, 0, "#6b6558", 0.95)] + layers,
                "filters": [{"type": "shadowmap", "amount": 0.65, "soft": 2, "size": 1024}, {"type": "atmos", "amount": 0.8, "density": 0.035, "falloff": 0.3, "shafts": 0.3}, {"type": "tonemap", "knee": 0.8}, {"type": "aa"}]}
    return {"background": "#020203", "camera": [cam(0, 1.25, -1.0, look=(0, 1.0, 8), zoom=1.0), cam(-5.5, 1.6, 2.0, look=(0.5, 1.2, 5.5), zoom=1.1)][(c.variant // 2) % 2],
            "layers": [lamp(0, 1.6, -1.2, 1.6, "#fff0d0", 14), floor(c, 0, "#151517", 0.9)] + layers,
            "filters": [{"type": "fog", "amount": 1.0, "density": 0.09, "color": "#020203"}, {"type": "tonemap", "knee": 0.7}, {"type": "aa"}, bloom(c, 0.5, 0.02, 0.7)]}


@idiom(needs=1, fam="travel", cost=2)
def lighthouse(c):
    """Lights on a dark coast, each turning once a riff. Their beams face you together only
    where the riffs do."""
    parts = c.riffs[:3]
    layers = [{"type": "stars", "count": 500, "speed": 0, "size": 0.8, "light": 0.5, "twinkle": 0.3, "streak": 0},
              lamp(-6, 8, -6, 0.25, "#8090b0"), {"type": "mesh", "shape": "plane", "detail": 4, "x": 0, "y": 0, "z": 0, "scale": 60, "material": "pbr", "rough": 0.25, "metal": 0.2, "color": "#0a0f18", "rim": 0, "cull": True}]
    for i, p in enumerate(parts):
        x, z = (i - (len(parts) - 1) / 2) * 3.4, 3 + 2.2 * i
        hgt = 2.3 - 0.2 * i
        th = f"(0.75 - {p.turn})"
        layers.append({"type": "mesh", "shape": "cylinder", "detail": 12, "x": x, "y": hgt / 2, "z": z, "scale": 1, "sx": 0.14, "sy": hgt / 2, "sz": 0.14, **solid("#d8d4cc", 0.7), "emit": 0.12})
        layers.append(ball(x, hgt + 0.1, z, 0.2, 10, **glow(c.col(i), f"1.5 + 3*{p.hit}")))
        for sgn in (1, -1):
            layers.append({"type": "beam", "from": [x, hgt + 0.1, z], "to": [f"{x} + {sgn}*7*cos({th})", hgt + 0.1, f"{z} + {sgn}*7*sin({th})"], "width": 0.05, "taper": -8, "glow": 1.0, "fade": 0.85, "color": c.col(i), "samples": 80})
    return {"background": "#020308", "camera": cam("0.6*sin(time.bar/12)", 1.2, -6.0, look=(0, 1.35, 3), zoom=1.75), "layers": layers,
            "filters": [{"type": "reflect", "y": 0, "amount": 0.5}, {"type": "tonemap", "knee": 0.7}, {"type": "aa"}, bloom(c, 0.6, 0.03, 0.6)]}


@idiom(needs=1, fam="travel", cost=2)
def stairs(c):
    """The tune is a staircase: each note a tread as high as its pitch, going by; someone
    walks it, always at the tread that is sounding."""
    T = (c.tunes + c.riffs)[0]
    lo, hi = 0.4, 3.4
    y = T.pitch(lo, hi)
    cur = T.pitch(lo, hi, f"(track.{T.name}.key*84 + 24)")
    w = 0.5
    layers = [{"type": "sky", "zenith": "#20304f", "horizon": c.b, "ground": "#141418", "sun": "#fff0d0", "sun_yaw": 0.3, "sun_height": 0.07},
              floor(c, 0, "#2c2c33", 0.9),
              box(f"0 - {w * 4:g}*note.age + {w}*clamp(note.len*4, 1, 8)", f"({y})/2", 0, f"{w}*clamp(note.len*4, 1, 8) - 0.02", f"({y})/2", 0.7, notes={"track": T.name, "past": 10, "ahead": 10},
                  **solid("#c9c3b6", 0.85), emit="0.5*note.on"),
              {"type": "figure", "rig": "human", "motion": "walk", "x": 0.15, "y": f"{cur} + 0.5", "z": 0, "scale": 0.48, "ry": 0.25, **skin(c.a, 0.6)}]
    return {"background": "#141418", "vars": {}, "camera": cam("0.5", 2.3, -8.5, look=(0.5, 1.9, 0), zoom=1.5), "layers": layers,
            "filters": [{"type": "shadowmap", "amount": 0.6, "soft": 2, "size": 1024}, {"type": "ao", "amount": 0.5, "radius": 0.06}, {"type": "tonemap", "knee": 0.8}, {"type": "aa"}, bloom(c, 0.3, 0.02, 0.85)]}


@idiom(needs=2, fam="room", cost=3)
def henge(c):
    """Two rings of stones, as many in each as a riff has sixteenths, and a sun that goes
    round once for every round of the two together: it stands in the gate when they meet."""
    A, B = c.riffs[0], c.riffs[1]
    L = math.lcm(A.cell, B.cell)
    yaw = f"(0.5 + (time.beat*4 - {A.anchor:g})/{L})"
    layers = [{"type": "sky", "zenith": "#1f2f55", "horizon": c.a, "ground": "#2a2a22", "sun": "#fff2d0", "sun_yaw": yaw, "sun_height": 0.045, "sun_size": 0.05, "glow": 1.5},
              floor(c, 0, "#56513f", 0.95)]
    for p, r, hgt, col in ((A, 1.7, 0.75, c.b), (B, 3.0, 1.0, c.c)):
        nn = p.cell
        d = f"(fract({p.turn} - inst.i/{nn})*{nn})"
        th = f"(inst.i/{nn} + 0.25 + {0.5 / nn})"
        layers.append(box(f"{r}*cos({th})", hgt, f"{r}*sin({th})", min(0.3, 2.2 * r / nn), hgt, 0.13, count=nn, ry=f"0.25 - {th}", round=0.12, **solid("#8d897c", 0.95), emit=f"0.5*exp(0 - 1.2*{d})*{p.hit}",
                         paint=f"exp(0 - 1.2*{d})*{p.hit}", paint_color=col))
    return {"background": "#1f2f55", "camera": [cam("0.7*sin(time.bar/9)", 0.85, -6.6, look=(0, 0.9, 0), zoom=1.2), cam(0, 7.5, -5.5, look=(0, 0.2, 0), zoom=1.5), cam(-1.3, 0.5, -1.0, look=(1.5, 1.0, 2.5), zoom=0.9)][c.variant % 3], "layers": layers,
            "filters": [{"type": "shadowmap", "amount": 0.75, "soft": 2, "size": 1024}, {"type": "atmos", "amount": 0.7, "density": 0.05, "falloff": 0.5, "shafts": 0.8}, {"type": "tonemap", "knee": 0.8}, {"type": "aa"}, bloom(c, 0.3, 0.03, 0.85)]}


# ───────────────────────── growing things and signs ─────────────────────────

@idiom(needs=1, fam="grow", paper=True)
def sunflower(c):
    """A seed head with as many arms as the riff has sixteenths, each arm lit in its turn;
    the angle between seeds drifts, and the arms wind and unwind."""
    A = c.riffs[0]
    N = 420
    g = f"({1 / A.cell:.6f} + 0.0045*sin(time.bar/8))"
    r = "(0.12*sqrt(inst.i + 1))"
    th = f"(inst.i*{g} + 0.25)"
    d = f"(fract({A.turn} - inst.i/{A.cell})*{A.cell})"
    layers = [ball(f"{r}*cos({th})", f"{r}*sin({th})", 0, f"(0.03 + 0.0022*sqrt(inst.i))*(1 + 0.7*exp(0 - 1.5*{d}))", 6, count=N, **glow(c.ink, f"0.18 + 1.6*exp(0 - 1.3*{d})"))]
    if len(c.riffs) > 1:
        B = c.riffs[1]
        d2 = f"(fract({B.turn} - inst.i/{B.cell})*{B.cell})"
        layers.append(ball(f"{r}*cos({th})", f"{r}*sin({th})", -0.05, f"0.02*exp(0 - 1.5*{d2})", 6, count=N, **glow(c.a, 2.5)))
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.35, 0.016, 0.6)]}


@idiom(needs=0, tune=True, fam="sign", cost=2)
def wires(c):
    """Five wires at dusk: the tune's notes come down on them as birds, each on the wire its
    pitch gives it, and the poles go by a bar apart."""
    T = (c.tunes + c.riffs + c.parts)[0]
    layers = [{"type": "gradient", "palette": ["#f6c58a", c.a, "#3a2a50", "#0c0a18"], "angle": 0.25, "spread": 0.95, "res": 0.5}]
    span = 6.4
    dark = {"color": "#050408", "light": 0, "ambient": 0, "rim": 0}
    # Each wire hangs between poles a bar apart: forty short lengths of it across the frame.
    sagx = lambda x: f"(0.22*(1 - pow(2*fract(({x} + {span / 2} + 64*{span})/{span}) - 1, 2)))"  # noqa: E731
    for k in range(5):
        layers.append(box(f"inst.i*0.25 - 5", f"{-1.5 + 0.62 * k:g} - {sagx('(inst.i*0.25 - 5 + fract(time.bar)*' + str(span) + ')')}", 0, 0.13, 0.008, 0.008, count=41, **dark))
    layers.append(box(f"(inst.i - 1)*{span} + {span / 2} - fract(time.bar)*{span}", -0.4, 0.05, 0.05, 2.4, 0.02, count=4, **dark))
    wire = f"floor({T.pitch(0, 4.99)})"
    x = "(3.9 - 1.5*note.age)"
    land = "smooth(0.0, 0.6, note.age)"
    layers.append({"type": "figure", "rig": "bird", "motion": "flap", "energy": f"1 - {land}", "notes": {"track": T.name, "past": 6, "ahead": 0.6}, "count": 48,
                   "x": x, "y": f"{-1.5:g} + 0.62*{wire} - {sagx(x + ' + fract(time.bar)*' + str(span))} + 0.13 + 1.6*(1 - {land})", "z": -0.05, "scale": 0.5, "ry": 0.3, **dark, "thick": 1.5})
    return {"background": "#0c0a18", "camera": FLAT, "layers": layers, "filters": [{"type": "vignette", "amount": 0.3}]}


@idiom(needs=1, fam="sign")
def marquee(c):
    """Bulbs round the frame chase at the riff's pace, a bulb a sixteenth, with another row
    inside going the other way for a second riff."""
    layers = []
    for i in range(5):
        p = c.riffs[i % len(c.riffs)]
        W, H = 4.15 - 0.47 * i, 2.25 - 0.47 * i
        per = 4 * (W + H)
        nn = max(p.cell, round(per / 0.3 / p.cell) * p.cell)
        s = f"(fract((inst.i + 0.5)/{nn})*{per:g})"
        # Round the rectangle: along the top, down the right, back along the bottom, up the left.
        x = f"(clamp({s}, 0, {2 * W}) - {W} - clamp({s} - {2 * W + 2 * H:g}, 0, {2 * W}))"
        y = f"({H} - clamp({s} - {2 * W}, 0, {2 * H}) + clamp({s} - {4 * W + 2 * H:g}, 0, {2 * H}))"
        d = f"(fract({'0 - ' if i % 2 else ''}{p.turn} - inst.i/{p.cell})*{p.cell})"
        layers.append(ball(x, y, 0, f"0.08 + 0.045*exp(0 - 1.5*{d})", 8, count=nn, **glow(c.col(i % len(c.riffs)), f"0.38 + 2.8*exp(0 - 1.3*{d})")))
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.55, 0.025, 0.45)]}


RULES = {3: 30, 4: 90, 5: 110, 6: 150, 7: 73, 8: 105, 9: 45, 10: 60, 11: 22, 12: 126, 13: 54, 14: 182, 15: 18, 16: 90}


@idiom(needs=1, fam="grow")
def automaton(c):
    """A row of cells that makes its next generation on every note of the riff; which rule
    it grows by goes with the riff's length."""
    A = c.riffs[0]
    layers = [{"type": "ca", "rule": RULES.get(A.cell, 110), "rate": f"{4 * c.bpm / 60:g}", "on": f"track.{A.name}", "cells": 16 * 4, "rows": 36, "width": 3.5, "height": 1.95, "fill": 0.86, "spread": 0.3, "fade": 0.75, "flash": 1,
               "start": "center", "palette": [c.ink, c.a, c.b, c.dim]}]
    f = [{"type": "mirror", "axis": "x"}] if c.variant % 2 else []
    return {"background": c.bg, "layers": layers, "filters": f + [bloom(c, 0.3, 0.012, 0.6)]}


@idiom(needs=0, fam="chaos")
def bifurcate(c):
    """One map, its one number turned slowly up: a single line splits in two, in four, in
    eight, and breaks into dust, with clear windows of three, five and seven in it."""
    layers = [{"type": "attractor", "kind": "logistic", "lo": 2.9, "hi": 4.0, "upto": f"3.35 + 0.66*{c.prog}", "points": 70000, "size": 1.6, "gain": "1.6 + 1.8*audio.low", "spread": 0.45, "palette": [c.ink, c.a, c.b]}]
    return {"background": c.bg, "layers": layers, "filters": [bloom(c, 0.3, 0.012, 0.6)]}


@idiom(needs=1, fam="chaos")
def strange(c):
    """A cloud of points drawn by a map whose numbers the riffs turn: it folds into a new
    figure with every note."""
    A = c.riffs[0]
    B = c.riffs[1] if len(c.riffs) > 1 else A
    sets = (("clifford", -1.4, 1.6, 1.0, 0.7), ("dejong", 1.4, -2.3, 2.4, -2.1), ("clifford", 1.7, 1.7, 0.6, 1.2), ("dejong", 2.01, -2.53, 1.61, -0.33),
            ("clifford", -1.7, 1.3, -0.1, -1.2), ("dejong", -2.7, -0.09, -0.86, -2.2), ("clifford", 1.5, -1.8, 1.6, 0.9), ("dejong", -0.827, -1.637, 1.659, -0.943))
    kind, a, b, cc, d = sets[c.variant % len(sets)]
    layers = [{"type": "attractor", "kind": kind, "a": f"{n(a)} + 0.08*sin({A.turn}/4)", "b": f"{n(b)} + 0.08*cos({B.turn}/4)", "c": f"{n(cc)} + 0.06*{A.hit}", "d": f"{n(d)} + 0.06*{B.hit}", "points": 80000, "size": 0.84,
               "gain": "1.8 + 0.7*audio.low", "spread": 0.55, "rotate": "time.bar/32", "palette": [c.a, c.ink, c.b]}]
    return {"background": c.bg, "layers": layers, "filters": [bloom(c, 0.35, 0.014, 0.6)]}


@idiom(needs=1, fam="field", paper=True)
def pond(c):
    """Still water: every note is a drop, set down across it at its place in the riff, and
    its ring spreads until the next ones cross it."""
    parts = (c.riffs + c.drums)[:3]
    layers = [{"type": "gradient", "palette": [c.bg, c.bg, "#0d1420" if not c.paper else c.bg], "radial": 1, "spread": 0.8, "res": 0.5}]
    for i, p in enumerate(parts):
        nn = p.cell or 16
        layers.append({"type": "shape", "notes": {"track": p.name, "past": 5}, "sides": 48, "radius": "0.03 + 0.3*note.age", "width": "0.006 + 0.02*exp(0 - 0.9*note.age)", "fill": 0,
                       "opacity": "exp(0 - 0.45*note.age)", "color": c.col(i), "x": f"({p.nstep} - {(nn - 1) / 2})*{min(0.5, 3.0 / nn):g}", "y": (i - (len(parts) - 1) / 2) * 0.55})
    return {"background": c.bg, "layers": layers, "filters": [{"type": "warp", "amount": 0.006, "scale": 5, "speed": 0.2}, bloom(c, 0.3, 0.014, 0.6)]}


SYL = {1: ["TA"], 2: ["TA", "KA"], 3: ["TA", "KI", "TA"], 4: ["TA", "KA", "DI", "MI"], 5: ["TA", "DI", "GI", "NA", "THOM"]}


def syllables(n_):
    """A riff's sixteenths as a drummer says them: in fours, with a three or a five to finish."""
    out = []
    while n_ > 0:
        k = n_ if n_ <= 5 else 3 if n_ in (6, 7) and not out else 4 if n_ - 4 != 1 else 3
        if n_ == 6:
            k = 3
        out += SYL[k]
        n_ -= k
    return out


@idiom(needs=1, fam="sign", paper=True, max_cell=16)
def solkattu(c):
    """Each riff said aloud: its sixteenths as spoken syllables in a row, the one sounding
    now lit."""
    parts = [p for p in c.riffs if p.cell <= 16][:3]
    if not parts:
        raise ValueError("too long to say")
    layers = []
    for i, p in enumerate(parts):
        syl = syllables(p.cell)
        cap = (0.6, 0.36, 0.26)[len(parts) - 1]
        size = min(cap, 3.4 / (len(syl) * 2.7))
        gap = cap * 2.15
        y = (len(parts) - 1) / 2 * gap - gap * i - size / 2
        for k, sy in enumerate(syl):
            d = f"(fract({p.turn} - {k / p.cell:.5f})*{p.cell})"
            for col, op in ((c.ink, "0.5"), (c.col(i), f"exp(0 - 1.6*{d})")):
                layers.append({"type": "text", "text": sy, "size": f"{size:g}*(1 + 0.25*exp(0 - 2*{d}))", "x": (k - (len(syl) - 1) / 2) * size * 2.7, "y": y, "align": "center", "width": 0.18, "skew": 0,
                               "color": col, "opacity": op})
    return {"background": c.bg, "layers": layers, "filters": [bloom(c, 0.25, 0.012, 0.7)]}


def signal(c):
    """The sound itself on a tube: the trace of now over the traces it has just drawn."""
    layers = [{"type": "shape", "sides": 4, "rotate": 0.125, "radius": 1.25, "width": 0.003, "fill": 0, "color": c.dim, "count": 1, "opacity": 0.5},
              {"type": "scope", "mode": "xy" if c.variant % 2 else "wave", "gain": 2.2, "width": 0.005, "size": 2.6 if c.variant % 2 == 0 else 1.5, "color": c.a, "points": 1600}]
    return {"background": c.bg, "layers": layers, "filters": [{"type": "expose", "open": 1, "fade": 0.5, "live": 1, "mode": "light"}, bloom(c, 0.4, 0.016, 0.5)]}


@idiom(needs=0, fam="trace")
def ridges(c):
    """A range of hills made of the sound: each ridge is the spectrum a moment ago, the
    nearest the newest."""
    layers = [{"type": "gradient", "palette": [c.bg, c.bg, c.a], "angle": 0.25, "spread": 0.35, "light": 0.5, "res": 0.5},
              {"type": "lines", "every": f"{c.six * 2:g}", "height": 1.5, "y": 0.5, "size": 1.7, "spacing": 0.036, "width": 0.007, "rows": 44, "palette": [c.dim, c.ink, c.ink], "spread": 0.5}]
    return {"background": c.bg, "layers": layers, "filters": [bloom(c, 0.25, 0.012, 0.7)]}



# ───────────────────────── more machines ─────────────────────────

@idiom(needs=1, fam="engine", cost=2, max_cell=13)
def radial(c):
    """A radial engine with a cylinder for each sixteenth of the riff: the crank goes round
    once a turn, and the pistons follow one another round the ring."""
    A = c.riffs[0]
    nn = max(3, min(A.cell, 13))
    rc, rod, R0 = 0.45, 1.25, 1.0
    th = f"(0.25 - {A.turn})"
    phi = f"(inst.i/{nn} + 0.25)"
    rel = f"({th} - {phi})"
    d = f"({rc}*cos({rel}) + sqrt({rod * rod:g} - {rc * rc:g}*pow(sin({rel}), 2)))"
    fire = f"exp(0 - 1.6*fract({A.turn} - inst.i/{nn})*{nn})"
    layers = [lamp(-3, 4, -7, 1.5),
              # The cylinders, the pistons in them, and the rods to the crank.
              box(f"{R0 + 1.05}*cos({phi})", f"{R0 + 1.05}*sin({phi})", 0.1, 0.6, 0.27, 0.12, count=nn, rz=phi, **solid("#3b3d44", 0.5, 0.8)),
              box(f"({d} + 0.3)*cos({phi})", f"({d} + 0.3)*sin({phi})", 0, 0.16, 0.2, 0.16, count=nn, rz=phi, **solid("#c9c5ba", 0.3, 0.9), emit=f"0.9*{fire}*{A.hit}"),
              {"type": "beam", "count": nn, "from": [f"{rc}*cos({th})", f"{rc}*sin({th})", -0.15], "to": [f"({d} + 0.2)*cos({phi})", f"({d} + 0.2)*sin({phi})", -0.15], "width": 0.035, "glow": 0.45, "color": c.dim, "samples": 12},
              ball(f"{rc}*cos({th})", f"{rc}*sin({th})", -0.2, 0.13, 10, **solid(c.a, 0.3, 0.9), emit=0.5),
              {"type": "mesh", "shape": "cylinder", "detail": 24, "x": 0, "y": 0, "z": 0.25, "scale": 1, "sx": 0.75, "sy": 0.08, "sz": 0.75, "rx": 0.25, **solid("#2b2c31", 0.6, 0.6)},
              ball(f"({R0 + 1.75})*cos({phi})", f"({R0 + 1.75})*sin({phi})", 0, f"0.07 + 0.12*{fire}*{A.hit}", 8, count=nn, **glow(c.b, f"0.2 + 3*{fire}*{A.hit}"))]
    return {"background": c.bg, "camera": cam(0, 0, -9, zoom=2.6, roll=f"{A.turn}/{nn * 8}"), "layers": layers, "filters": post3d(-3, 4, -7, shadow=0.5)}


@idiom(needs=2, fam="orbit", cost=2)
def armillary(c):
    """Rings within rings, each turning on its own axis once a riff: they lie flat in one
    plane together only where the riffs meet."""
    parts = c.riffs[:4]
    layers = [lamp(-3, 5, -6, 1.8), lamp(4, -2, -5, 0.85, c.a), lamp(0, 3, -7, 0.5, c.b), ball(0, 0, 0, 0.28, 14, **glow(c.b, 2.4))]
    for i, p in enumerate(parts):
        ax = ("rx", "rz", "rx", "rz")[i]
        layers.append({"type": "mesh", "shape": "torus", "detail": 56, "x": 0, "y": 0, "z": 0, "scale": 1.15 + 0.62 * i, "tube": 0.052 - 0.005 * i, ax: p.turn, "ry": 0.07 * i,
                       **solid(("#d8b468", "#c8c2b4", "#d89a68", "#9eb2c4")[i], 0.28, 0.88), "emit": f"0.14 + 0.45*{p.hit}"})
    return {"background": c.bg, "camera": cam("5.6*sin(time.bar/20)", 2.2, "0 - 5.6*cos(time.bar/20)", zoom=1.9), "layers": layers, "filters": post3d(-3, 5, -6, shadow=0.4)}


@idiom(needs=2, fam="clock", cost=2)
def clockfield(c):
    """A wall of small clocks, each with two hands, one for each of two riffs. A hand stands
    at its riff's place in its turn, and each clock is set a little on from the one before
    it: along the wall for the first riff, down it for the second (or out from the middle
    and round it, or along the two diagonals). So each riff is a wave of hands going over
    the wall, a crossing to a turn, stepping on the sixteenth, and a line of light goes
    with each where the hands pass twelve. The clocks are set less far apart the nearer
    the two riffs are to coming round together: when they do, every clock on the wall
    reads noon."""
    A, B = c.riffs[0], c.riffs[1]
    cols, rows = 16, 9
    dx, dy = 8.4 / cols, 4.6 / rows
    R = 0.47 * min(dx, dy)
    ci = f"floor(fract((inst.i + 0.5)/{cols})*{cols})"
    ri = f"floor(inst.i/{cols})"
    x0 = f"(({ci} - {(cols - 1) / 2:g})*{dx:g})"
    y0 = f"(({(rows - 1) / 2:g} - {ri})*{dy:g})"
    u, v = f"({ci}/{cols})", f"({ri}/{rows})"                      # 0..1 across and down
    rad = f"(sqrt(pow({ci} - {(cols - 1) / 2:g}, 2) + pow(({ri} - {(rows - 1) / 2:g})*{dy / dx:g}, 2))/{cols / 2:g})"
    ang = f"(atan2(({ci} - {(cols - 1) / 2:g})*{dx:g} + 0.001, ({(rows - 1) / 2:g} - {ri})*{dy:g}))"
    offs = ((u, v), (rad, ang), (f"(({u} + {v})/2)", f"(({u} - {v})/2)"), (f"(2*abs({u} - 0.47))", f"(2*abs({v} - 0.44))"))[c.seed % 4]
    # How far the riffs are from coming round together (0 there, 1 well away).
    near = lambda p: f"min(fract({p.turn}), 1 - fract({p.turn}))"
    apart = f"smooth(0, 0.3, max({near(A)}, {near(B)}))"
    layers = [ball(x0, y0, 0.02, 0.028, 5, count=cols * rows, **glow(c.dim, 1.1))]
    for k, (p, off) in enumerate(((A, offs[0]), (B, offs[1]))):
        nn = p.cell or 16
        st = f"({p.turn}*{nn})"
        ph = f"((floor({st}) + smooth(0.5, 1, fract({st})))/{nn} + {apart}*{off})"
        a = f"(0.25 - {ph})"
        # (Light as the hand passes twelve, and a little on each of the riff's notes.)
        lit = f"0.5 + 1.9*exp(0 - 7*fract({ph})) + 0.5*{p.hit}"
        layers.append(box(f"{x0} + {R / 2:g}*cos({a})", f"{y0} + {R / 2:g}*sin({a})", -0.02 * k, R / 2, 0.03, 0.01, count=cols * rows, rz=a,
                          **glow(c.col(k), lit)))
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.4, 0.014, 0.6)]}


@idiom(needs=1, fam="clock", cost=2)
def clockshop(c):
    """A wall of dials, one for every part that keeps a riff, each with as many hours as its
    riff has sixteenths and a hand that steps one a sixteenth."""
    names, P = set(), []
    for p in c.every + c.drums:
        if p.name not in names and p.cell and p.cell <= 48:
            names.add(p.name), P.append(p)
    P = P[:8]
    cols = min(4, len(P)) if len(P) != 2 else 2
    rows = math.ceil(len(P) / cols)
    R = min(1.9, 3.9 / cols, 2.15 / rows) * 0.9
    layers = []
    for i, p in enumerate(P):
        x0 = ((i % cols) - (cols - 1) / 2) * (8.4 / cols)
        y0 = ((rows - 1) / 2 - i // cols) * (4.5 / rows)
        nn = p.cell
        col = c.col(i)
        layers.append(box(f"{x0:g} + {R}*cos(inst.i/{nn} + 0.25)", f"{y0:g} + {R}*sin(inst.i/{nn} + 0.25)", 0, 0.035, 0.11 * R / 0.9, 0.01, count=nn, rz=f"inst.i/{nn}", **glow(c.ink, 0.9)))
        a = f"(0.25 - floor({p.turn}*{nn} + 0.02)/{nn})"
        layers.append(box(f"{x0:g} + {0.42 * R:g}*cos({a})", f"{y0:g} + {0.42 * R:g}*sin({a})", -0.05, 0.42 * R, 0.06, 0.01, rz=a, **glow(col, f"0.9 + 1.2*{p.hit}")))
        layers.append(ball(x0, y0, -0.06, 0.1, 8, **glow(col, 1)))
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.35, 0.014, 0.6)]}


@idiom(needs=1, fam="count", cost=2, max_cell=16)
def abacus(c):
    """A frame of beads: each rod is a riff, with a bead for each of its sixteenths, and the
    beads go across one by one and all come back when the riff comes round."""
    P = [p for p in c.riffs if p.cell <= 16][:4]
    if not P:
        raise ValueError("no rod")
    layers = [lamp(-2, 4, -7, 1.5), box(0, 0, 0.35, 4.3, 0.42 + 0.45 * len(P), 0.05, **solid("#141416", 0.9))]
    for k in (-1, 1):
        layers.append(box(k * 4.2, 0, 0, 0.09, 0.42 + 0.45 * len(P), 0.14, **solid("#5a3b22", 0.6)))
    for i, p in enumerate(P):
        y = ((len(P) - 1) / 2 - i) * 0.9
        nn = p.cell
        w = min(0.34, 3.2 / nn)
        over = f"smooth(0, 0.6, {p.ph}*{nn} - inst.i)"       # has this bead gone across yet this turn?
        x = f"mix({-3.9 + w / 2:g} + inst.i*{w:g}, {3.9 - w / 2:g} - ({nn - 1} - inst.i)*{w:g}, {over})"
        layers.append(box(0, y, 0, 4.1, 0.018, 0.018, **solid("#8c8c94", 0.3, 0.9)))
        layers.append({"type": "mesh", "shape": "sphere", "detail": 12, "count": nn, "x": x, "y": y, "z": 0, "scale": 0.21, "sx": w / 0.44, "sy": 1, "sz": 1, **solid(c.col(i), 0.35), "emit": f"0.5*{p.hit}*step(abs({p.ph}*{nn} - inst.i - 0.5), 0.6)"})
    return {"background": c.bg, "camera": cam("0.6*sin(time.bar/9)", 0.3, -9, zoom=1.9), "layers": layers, "filters": post3d(-2, 4, -7)}


@idiom(needs=1, fam="swing", cost=2)
def metronomes(c):
    """Metronomes on one plank, each ticking a riff; the plank hangs on cords and sways a
    little with them all."""
    names, P = set(), []
    for p in c.every + c.drums:
        if p.name not in names and p.cell:
            names.add(p.name), P.append(p)
    P = P[:7]
    sway = "0.12*sin(time.bar/2)"
    layers = [lamp(-2, 5, -6, 1.5), floor(c, -1.6, "#1b1b1f", 0.8), box(sway, -0.52, 0, 0.5 * len(P) + 0.5, 0.04, 0.5, **solid("#7a5a3a", 0.7))]
    for k in (-1, 1):
        layers.append({"type": "beam", "from": [k * (0.5 * len(P) + 0.3), 3.2, 0], "to": [f"{sway} + {k * (0.5 * len(P) + 0.3):g}", -0.5, 0], "width": 0.008, "glow": 0.3, "color": c.dim})
    for i, p in enumerate(P):
        x = f"({sway} + {(i - (len(P) - 1) / 2) * 0.95:g})"
        a = f"(0.085*tri({p.turn}*{max(1, round(p.cell / 4))}/2 + 0.25))"
        layers.append({"type": "mesh", "shape": "cone", "detail": 4, "x": x, "y": 0.0, "z": 0, "scale": 0.5, "sx": 0.6, "sz": 0.5, "ry": 0.125, **solid("#40302a" if i % 2 else "#2e2a34", 0.6)})
        layers.append(box(f"{x} + 0.75*sin({a})", f"-0.35 + 0.75*cos({a})", -0.3, 0.012, 0.75, 0.012, rz=f"0 - {a}", **solid("#c8c8cc", 0.3, 0.9)))
        layers.append(box(f"{x} + {1.0 - 0.02 * (p.cell % 16):g}*sin({a})", f"-0.35 + {1.0 - 0.02 * (p.cell % 16):g}*cos({a})", -0.32, 0.06, 0.07, 0.03, rz=f"0 - {a}", **solid(c.col(i), 0.4, 0.5), emit=f"0.8*{p.hit}"))
    look = {"background": c.bg, "layers": layers, "filters": post3d(-2, 5, -6)}
    return shots(c, look, [cam("0.7*sin(time.bar/8)", 0.4, -6.5, look=(0, 0.0, 0), zoom=2.5), cam(-3.0, 1.2, -5.0, look=(0, 0.1, 0), zoom=2.2)], P[0])


@idiom(needs=1, fam="fair", cost=2, max_cell=24)
def ferris(c):
    """A wheel at a night fair with a car for each sixteenth of the riff, going round once a
    turn; a second wheel behind keeps another riff."""
    layers = [{"type": "stars", "count": 300, "speed": 0, "size": 0.8, "light": 0.4, "twinkle": 0.3, "streak": 0}, lamp(0, 6, -6, 0.5), floor(c, -2.5, "#101014", 0.5)]
    for i, p in enumerate(c.riffs[:2]):
        nn = min(p.cell, 24)
        R, x0, z0 = (1.9, -1.4, 0) if i == 0 else (1.45, 2.4, 1.5)
        y0 = R - 2.3
        th = f"(inst.i/{nn} + {'0 - ' if i else ''}{p.turn}/{nn} + 0.25)"
        px, py = f"{x0} + {R}*cos({th})", f"{y0:g} + {R}*sin({th})"
        d = f"(fract({p.turn} - inst.i/{nn})*{nn})"
        layers.append({"type": "beam", "count": nn, "from": [x0, y0, z0], "to": [px, py, z0], "width": 0.008, "glow": 0.5, "color": c.dim})
        layers.append({"type": "mesh", "shape": "torus", "detail": 60, "x": x0, "y": y0, "z": z0, "scale": R / 0.8, "tube": 0.012, "rx": 0.25, **glow(c.col(i), 0.9)})
        layers.append(box(px, f"{py} - 0.16", z0, 0.1, 0.09, 0.08, count=nn, **solid(c.col(i + 1), 0.5), emit=f"0.25 + 1.6*exp(0 - 1.5*{d})"))
        layers.append(box(x0, (y0 - 2.5) / 2, z0 + 0.1, 0.05, (y0 + 2.5) / 2, 0.05, **solid("#34343a", 0.6)))
    return {"background": "#030308", "camera": cam("0.8*sin(time.bar/10)", -0.4, -7.5, look=(0.3, -0.3, 0), zoom=1.5), "layers": layers,
            "filters": [{"type": "reflect", "y": -2.5, "amount": 0.35}, {"type": "tonemap", "knee": 0.7}, {"type": "aa"}, bloom(c, 0.6, 0.025, 0.55)]}


@idiom(needs=1, fam="fair", cost=3, max_cell=16)
def carousel(c):
    """A roundabout with a horse for each sixteenth of the riff, each rising as its turn
    comes; the whole goes round once in as many turns."""
    A = c.riffs[0]
    nn = max(3, min(A.cell, 16))
    spin = f"({A.turn}/{nn})"
    th = f"(inst.i/{nn} + {spin})"
    up = f"(0.3*exp(0 - 0.8*fract({A.turn} - inst.i/{nn})*{nn}))"
    import studies as S
    layers = [lamp(0, 3.0, 0, 1.6, "#ffe2b0", 9), lamp(-4, 5, -6, 0.6),
              floor(c, 0, "#16161a", 0.6),
              {"type": "mesh", "shape": "cylinder", "detail": 40, "x": 0, "y": 0.1, "z": 0, "scale": 1, "sx": 2.6, "sy": 0.1, "sz": 2.6, **solid("#7a2e2a", 0.6)},
              {"type": "mesh", "shape": "cone", "detail": 40, "x": 0, "y": 3.5, "z": 0, "scale": 1, "sx": 2.9, "sy": 0.5, "sz": 2.9, **solid(c.a, 0.6)},
              {"type": "mesh", "shape": "cylinder", "detail": 12, "x": 0, "y": 1.6, "z": 0, "scale": 1, "sx": 0.12, "sy": 1.6, "sz": 0.12, **solid("#d8c890", 0.3, 0.9)},
              {"type": "mesh", "shape": "cylinder", "detail": 6, "count": nn, "x": f"2.0*cos({th})", "y": 1.6, "z": f"2.0*sin({th})", "scale": 1, "sx": 0.02, "sy": 1.5, "sz": 0.02, **solid("#d8c890", 0.3, 0.9)},
              {"type": "figure", "bones": S.horse_bones(), "motion": "none", "pose": S.horse_pose("gallop"), "phase": f"2*{A.turn} + inst.i", "count": nn, "x": f"2.0*cos({th})", "y": f"0.95 + {up}", "z": f"2.0*sin({th})",
               "scale": 0.55, "ry": f"0 - {th}", "thick": 0.85, **skin(c.ink, f"0.5*{up}")},
              ball(f"2.75*cos(inst.i/24 + {spin})", 3.05, f"2.75*sin(inst.i/24 + {spin})", 0.05, 6, count=24, **glow(c.b, 2.2))]
    look = {"background": "#04040a", "layers": layers, "filters": post3d(0, 3.0, 0, shadow=0.5, thr=0.8, glow=0.5)}
    return shots(c, look, [cam(0, 1.6, -7.8, look=(0, 1.5, 0), zoom=1.45), cam(0.6, 0.9, -4.0, look=(0, 1.4, -1.6), zoom=1.2)], A)


@idiom(needs=1, fam="field3", cost=3)
def turbines(c):
    """A field of windmills, a row for each part: every sail turns once a riff, each mill a
    step behind its neighbour."""
    P = (c.riffs + c.drums)[:3]
    layers = [{"type": "sky", "zenith": "#3a66a8", "horizon": "#dfe9ee", "ground": "#6f7f52", "sun": "#fff4dc", "sun_yaw": 0.35, "sun_height": 0.09, "clouds": 0.35}, floor(c, 0, "#72844f", 0.95)]
    for i, p in enumerate(P):
        nn = 7
        z = 2.5 + 4.2 * i
        x = f"(inst.i - {(nn - 1) / 2})*{2.6 + 0.9 * i:g} + {0.9 * (i % 2):g}"
        layers.append({"type": "mesh", "shape": "cylinder", "detail": 8, "count": nn, "x": x, "y": 1.5, "z": z, "scale": 1, "sx": 0.06, "sy": 1.5, "sz": 0.06, **solid("#eeeeea", 0.5)})
        for b in range(3):
            a = f"({p.turn} - inst.i/{p.cell} + {b / 3:.4f})"
            layers.append(box(f"{x} + 0.75*cos({a})", f"3.0 + 0.75*sin({a})", z - 0.1, 0.75, 0.05, 0.015, count=nn, rz=a, **solid("#f4f4f0" if b else c.col(i), 0.5)))
    return {"background": "#dfe9ee", "camera": cam("1.5*sin(time.bar/14)", 2.0, -6, look=(0, 2.4, 5), zoom=1.3), "layers": layers,
            "filters": [{"type": "shadowmap", "amount": 0.6, "soft": 2, "size": 1024}, {"type": "atmos", "amount": 0.7, "density": 0.03, "falloff": 0.4, "shafts": 0.2}, {"type": "tonemap", "knee": 0.8}, {"type": "aa"}]}


@idiom(needs=1, fam="machine", cost=2)
def keys(c):
    """A keyboard played by the riffs: each note puts its own key down for as long as it sounds."""
    P = (c.riffs + c.tunes)[:3]
    lo = min(p.lo for p in P)
    hi = max(p.hi for p in P)
    lo, hi = int(lo) - 1, max(int(hi) + 2, int(lo) + 14)
    nn = hi - lo
    w = min(0.3, 8.6 / nn)
    black = "(step(0.5, fract((inst.i + {0})*7/12 + 0.01)*12/7 - 1) * 0 + step(0.58, fract((inst.i + {0} + 0.5)*7/12)))".format(lo % 12)
    x = f"(inst.i - {(nn - 1) / 2})*{w:g}"
    layers = [lamp(-2, 5, -5, 0.8), box(0, -0.1, 0.9, 4.6, 0.08, 1.2, **solid("#101012", 0.5)),
              box(x, 0, 0, w * 0.46, 0.06, 0.8, count=nn, **solid("#a8a59c", 0.4)),
              box(x, f"0.07*{black} - 0.2*(1 - {black})", 0.3, w * 0.3, 0.08, 0.5, count=nn, **solid("#0c0c0e", 0.3))]
    for i, p in enumerate(P):
        layers.append(box(f"(note.midi - {lo} - {(nn - 1) / 2})*{w:g}", "0.075 - 0.05*note.on", -0.25, w * 0.4, 0.012, 0.5, notes={"track": p.name, "past": 4}, **glow(c.col(i), "2.5*exp(0 - 1.4*max(0 - note.left, 0))"),
                          opacity="exp(0 - 1.4*max(0 - note.left, 0))"))
    look = {"background": c.bg, "layers": layers, "filters": post3d(-2, 5, -5)}
    return shots(c, look, [cam("1.2*sin(time.bar/9)", 2.3, -3.6, look=(0, 0, 0.1), zoom=1.25), cam(0, 6.5, -0.3, look=(0, 0, 0.1), zoom=1.75), cam(-5.2, 0.7, -1.0, look=(0, 0, 0), zoom=1.6)], P[0])


@idiom(needs=0, fam="swarm")
def fireflies(c):
    """A ring of fireflies, each with its own pace, drawn into step as the scene goes on and
    scattered again by the drum."""
    on = (c.snare or c.kick or (c.parts[0] if c.parts else None))
    layers = []
    for k in range(3):
        layer = {"type": "swarm", "count": 160 - 40 * k, "coupling": f"0.05 + {3.2 - 0.8 * k:g}*{c.prog}", "spread": 0.7, "speed": f"{c.bpm / 240 * (1 if k % 2 == 0 else -1):g}", "radius": 0.85 - 0.27 * k, "size": 0.014,
                 "soft": 0.7, "hues": 0.5, "order": 0.4, "palette": [c.col(k), c.col(k + 1), c.ink]}
        if on:
            layer.update({"kick": 0.5, "on": f"track.{on.name}"})
        layers.append(layer)
    return {"background": c.bg, "layers": layers, "filters": [bloom(c, 0.5, 0.02, 0.45)]}


@idiom(needs=0, fam="weather", cost=2)
def rain(c):
    """A wet street at night: the drops are the notes, and each leaves its ring."""
    P = (c.riffs + c.drums + c.parts)[:3]
    layers = [lamp(0, 4, 3, 1.4, c.a, 12), lamp(-4, 3, 5, 1.0, c.b, 10),
              {"type": "mesh", "shape": "plane", "detail": 4, "x": 0, "y": 0, "z": 0, "scale": 30, "material": "pbr", "rough": 0.12, "metal": 0.3, "color": "#0b0c10", "rim": 0, "cull": True},
              box(-2.6, 1.6, 6, 1.6, 1.6, 0.1, **glow(c.a, 1.2)), box(2.4, 1.1, 7, 1.2, 1.1, 0.1, **glow(c.b, 1.0)),
              {"type": "motes", "mode": "drift", "count": 400, "w": 9, "h": 5, "d": 7, "y": 2.5, "z": 2, "fall": 5, "wobble": 0.0, "size": 0.006, "glow": 0.5, "twinkle": 0, "color": c.dim}]
    for i, p in enumerate(P):
        nn = p.cell or 16
        layers.append({"type": "mesh", "shape": "torus", "detail": 32, "notes": {"track": p.name, "past": 3}, "x": f"({p.nstep} - {(nn - 1) / 2})*{min(0.7, 6.0 / nn):g}", "y": 0.01, "z": 0.6 + 1.5 * i,
                       "scale": "0.06 + 0.6*note.age", "tube": "0.12/(1 + 5*note.age)", **glow(c.col(i), "3*exp(0 - 1.0*note.age)")})
    return {"background": "#020204", "camera": cam("0.5*sin(time.bar/9)", 1.1, -4.2, look=(0, 0.5, 2), zoom=1.2), "layers": layers,
            "filters": [{"type": "reflect", "y": 0, "amount": 0.6}, {"type": "tonemap", "knee": 0.7}, {"type": "aa"}, bloom(c, 0.5, 0.03, 0.6)]}


@idiom(needs=1, fam="weather", cost=3)
def tide(c):
    """A sea made of two swells, one as long as each riff: where their crests fall together
    the big wave comes, and it comes round with the riffs."""
    A = c.riffs[0]
    B = c.riffs[1] if len(c.riffs) > 1 else A
    k = 6.0
    wave = (f"0.009*sin(vtx.z*{k * 16 / A.cell:g} + {A.turn}) + 0.009*sin(vtx.z*{k * 16 / max(B.cell, 2):g} + vtx.x*1.5 + {B.turn}) + 0.002*fbm(vtx.x*9, vtx.z*9, time.t*0.3)")
    layers = [{"type": "sky", "zenith": "#141c33", "horizon": c.b, "ground": "#05070c", "sun": "#fff0cc", "sun_yaw": 0.0, "sun_height": 0.035, "sun_size": 0.05, "glow": 1.4},
              {"type": "mesh", "shape": "plane", "detail": 150, "x": 0, "y": 0, "z": 6, "scale": 12, "material": "pbr", "rough": 0.18, "metal": 0.1, "color": "#0c2030", "rim": 0, "displace": wave, "shading": "pixel", "cull": True},
              ball(0.8, f"0.12 + 0.1*sin({A.turn}) + 0.1*sin({B.turn})", 3, 0.16, 12, **solid(c.a, 0.4), emit=0.5)]
    return {"background": "#141c33", "camera": cam(0, 0.9, -3.2, look=(0, 0.3, 4), zoom=1.2), "layers": layers,
            "filters": [{"type": "atmos", "amount": 0.6, "density": 0.04, "falloff": 0.6, "shafts": 0.4}, {"type": "tonemap", "knee": 0.75}, {"type": "aa"}, bloom(c, 0.3, 0.03, 0.85)]}


@idiom(needs=2, fam="field", paper=True)
def vortex(c):
    """Two spirals, one with an arm for each sixteenth of one riff and one for the other,
    wound opposite ways and laid together."""
    A, B = c.riffs[0], c.riffs[1]
    layers = [{"type": "rings", "count": 3.5, "speed": 0, "duty": 0.5, "soft": 0.03, "twist": A.cell, "tunnel": 0.35, "x": 0, "y": 0, "color": "#ffffff", "spread": 0},
              {"type": "rings", "count": 3.5, "speed": 0, "duty": 0.5, "soft": 0.03, "twist": -B.cell, "tunnel": 0.35, "x": f"0.12*cos({B.turn})", "y": f"0.12*sin({B.turn})", "color": "#ffffff", "spread": 0, "blend": "difference"}]
    return {"background": "#000000", "layers": layers, "filters": [{"type": "camera", "rotate": f"{A.turn}/{A.cell}", "zoom": 1.3}, {"type": "tint", "palette": [c.bg, c.b, c.ink], "amount": 1, "pos": 0}, bloom(c, 0.25)]}


@idiom(needs=2, fam="machine", paper=True, cost=2)
def kelvin(c):
    """A tide-predicting machine: a wheel for each riff with a pin on it, one cord over all
    the pins, and a pen on the cord's end that draws the sum of them on a moving paper."""
    P = c.riffs[:4]
    nn = len(P)
    r = 0.42
    xs = [(i - (nn - 1) / 2) * 1.55 - 1.2 for i in range(nn)]
    pins = [(f"{xs[i]:g} + {r}*cos(0.25 - {p.turn})", f"1.3 + {r}*sin(0.25 - {p.turn})") for i, p in enumerate(P)]
    total = " + ".join(f"{r}*sin(0.25 - {p.turn})" for p in P)
    pen_x, pen_y = xs[-1] + 1.6, f"(0 - 0.9 + 0.75*({total}))"
    layers = []
    for i, p in enumerate(P):
        layers.append({"type": "mesh", "shape": "torus", "detail": 40, "x": xs[i], "y": 1.3, "z": 0, "scale": (r + 0.14) / 0.8, "tube": 0.085, "rx": 0.25, **glow(c.dim, 1.35)})
        layers.append(ball(pins[i][0], pins[i][1], -0.05, 0.14, 8, **glow(c.col(i), f"1.4 + 1.8*{p.hit}")))
        layers.append({"type": "beam", "from": [xs[i], 1.3, 0], "to": [pins[i][0], pins[i][1], 0], "width": 0.016, "glow": 0.75, "color": c.dim})
    pts = [(f"{xs[0] - 1.3:g}", "1.3")] + pins + [(f"{pen_x:g}", pen_y)]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        layers.append({"type": "beam", "from": [x0, y0, -0.02], "to": [x1, y1, -0.02], "width": 0.028, "glow": 1.15, "color": c.ink, "samples": 30})
    layers.append({"type": "trail", "x": f"{pen_x:g} - 1.1*(var.nowb - time.beat)", "y": pen_y, "z": 0, "length": f"{6 * 0.5 / (c.bpm / 120):g}", "samples": 500, "width": 0.052, "taper": 0, "glow": 1.5, "fade": 0.5, "color": c.a})
    layers.append(ball(pen_x, pen_y, -0.05, 0.095, 8, **glow(c.a, 2.8)))
    return {"background": c.bg, "vars": {"nowb": {"follow": "time.beat", "attack": "0ms", "release": "0ms"}}, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.35, 0.016, 0.55)]}


@idiom(needs=2, fam="curve", paper=True)
def harmonograph(c):
    """A pen hung between two pendulums, one keeping each riff, their swings dying away: it
    draws one figure through the whole scene, closing in on its middle."""
    A, B = c.riffs[0], c.riffs[1]
    dur = (c.b16 - c.a16) / 4
    # (In a trail the song's clock is wound back, so everything here is written on time.beat.)
    age = f"(time.beat - {c.a16 / 4:g})"
    decay = f"exp(0 - 1.6*{age}/{dur:g})"
    x = f"3.3*{decay}*sin((time.beat*4 - {A.anchor:g})/{A.cell})"
    y = f"2.1*{decay}*sin((time.beat*4 - {B.anchor:g})/{B.cell} + 0.125)"
    layers = [{"type": "trail", "x": x, "y": y, "z": 0, "length": f"clamp(scene.t, 0.05, {dur * 0.5 / (c.bpm / 120):g})", "samples": 4000, "width": 0.011, "taper": 0, "glow": 0.9, "fade": 0.35, "color": c.ink},
              ball(x, y, -0.05, 0.06, 8, **glow(c.a, 3))]
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.3, 0.014, 0.6)]}


@idiom(needs=2, fam="lattice", paper=True)
def combs(c):
    """Two combs going by, the teeth of each a riff apart. Where a tooth of one stands over a
    tooth of the other there is a long mark: you can see the meeting coming."""
    A, B = c.riffs[0], c.riffs[1]
    L = math.lcm(A.cell, B.cell)
    u = 0.26
    layers = []

    def row(period, anchor, y, h, col, emit, z=0):
        k = int(9.4 / (period * u)) + 3
        x = f"((inst.i - {k // 2})*{period * u:g} - fract((time.beat*4 - {anchor:g})/{period})*{period * u:g})"
        near = f"exp(0 - 3*abs({x}))"
        layers.append(box(x, y, z, 0.045, h, 0.01, count=k, **glow(col, f"{emit} + 2.4*{near}")))
    # Horizontal comb spines tying each row of teeth together.
    layers.append(box(0, 0.75, 0.05, 4.6, 0.018, 0.01, **glow(c.a, "0.35 + 0.4*audio.low")))
    layers.append(box(0, -0.75, 0.05, 4.6, 0.018, 0.01, **glow(c.b, "0.35 + 0.4*audio.low")))
    row(1, 0, 0, 0.06, c.dim, 0.65)
    row(16, 0, 0, 0.28, c.dim, 0.85)
    row(A.cell, A.anchor, 0.75, 0.65, c.a, 0.85)
    row(B.cell, B.anchor, -0.75, 0.65, c.b, 0.85)
    # The round's own tooth: where both began together (or will).
    meet = next((s for s in range(L) if (s - A.anchor) % A.cell == 0 and (s - B.anchor) % B.cell == 0), None)
    if meet is not None:
        row(L, meet, 0, 1.75, c.ink, 1.15, z=-0.05)
    layers.append(box(0, 0, -0.02, 0.012, 2.5, 0.01, **glow(c.ink, f"0.55 + 1.2*max({A.hit}, {B.hit})")))
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.35, 0.016, 0.6)]}


@idiom(needs=2, fam="field3", cost=2)
def tiles(c):
    """A wall of tiles that turn over in waves: one wave runs across it as long as one riff,
    another down it as long as the other, and the pattern is their sum."""
    A, B = c.riffs[0], c.riffs[1]
    cols, rows = 32, 18
    ix, iy = f"(inst.i - {cols}*floor(inst.i/{cols}))", f"floor(inst.i/{cols})"
    a = f"(0.25*smooth(-0.3, 0.3, sin({A.turn} - {ix}/{A.cell}) + sin({B.turn} - {iy}/{B.cell})))"
    layers = [lamp(-3, 4, -7, 1.15), lamp(4, -1, -6, 0.85, c.a), lamp(0, 3, -5, 0.45, c.b),
              box(f"({ix} - {(cols - 1) / 2})*0.285", f"({iy} - {(rows - 1) / 2})*0.285", 0, 0.132, 0.132, 0.014, count=cols * rows, ry=a, **solid("#b4b0a8", 0.35, 0.72), emit=f"0.12 + 0.35*abs(sin({A.turn} - {ix}/{A.cell}) + sin({B.turn} - {iy}/{B.cell}))*0.5")]
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [{"type": "tonemap", "knee": 0.7}, {"type": "aa"}, bloom(c, 0.25, 0.012, 0.85)]}


@idiom(needs=1, fam="swing", cost=2, max_cell=12)
def belfry(c):
    """A ring of bells, one for each sixteenth of the riff: each is swung as its turn comes,
    and rings down until it comes again."""
    A = c.riffs[0]
    nn = max(3, min(A.cell, 12))
    d = f"(fract({A.turn} - inst.i/{nn})*{nn})"
    sw = f"(0.11*exp(0 - 0.35*{d})*cos({d}*0.8))"
    x = f"(inst.i - {(nn - 1) / 2})*{min(1.0, 7.6 / nn):g}"
    sz = min(0.42, 3.2 / nn)
    layers = [lamp(-2, 5, -6, 1.35), lamp(3, 0.5, -5, 0.75, c.a), lamp(0, -1, -5, 0.35, c.b), floor(c, -0.35, "#15161c", 0.5),
              box(0, 1.55, 0, 4.4, 0.08, 0.12, **solid("#4a3624", 0.75)),
              {"type": "mesh", "shape": "cone", "detail": 20, "count": nn, "x": f"{x} + 0.75*sin({sw})", "y": f"1.5 - 0.75*cos({sw})", "z": 0, "scale": sz * 1.32, "sy": 1.18, "rz": sw, **solid("#a88240", 0.35, 0.88),
               "emit": f"0.15 + 0.85*exp(0 - 0.9*{d})*{A.hit}"},
              ball(f"{x} + 0.96*sin({sw})", f"1.5 - 0.96*cos({sw})", 0, sz * 0.22, 8, count=nn, **glow(c.ink, f"0.35 + 2.2*exp(0 - 1.2*{d})")),
              {"type": "beam", "count": nn, "from": [x, 1.5, 0], "to": [f"{x} + 0.45*sin({sw})", f"1.5 - 0.45*cos({sw})", 0], "width": 0.016, "glow": 0.55, "color": c.dim}]
    return {"background": c.bg, "camera": cam("0.6*sin(time.bar/8)", 0.95, -6.2, look=(0, 0.9, 0), zoom=2.45), "layers": layers, "filters": post3d(-2, 5, -6, shadow=0.5)}


@idiom(needs=2, fam="swing", cost=2)
def mobile(c):
    """A hanging mobile: each arm turns once a riff under the one above it, with a painted
    leaf at its end."""
    P = c.riffs[:3]
    layers = [lamp(-2, 5, -6, 1.3), floor(c, -0.6, "#232328", 0.9)]
    px, py, pz = "0", 2.3, "0"
    Lk = [2.3, 1.5, 1.0]
    for i, p in enumerate(P):
        th = f"({p.turn}*{1 if i % 2 == 0 else -1})"
        y = py - 0.55
        layers.append({"type": "beam", "from": [px, py, pz], "to": [px, y, pz], "width": 0.008, "glow": 0.5, "color": c.dim})
        ex, ez = f"({px} + {Lk[i]}*cos({th}))", f"({pz} + {Lk[i]}*sin({th}))"
        fx, fz = f"({px} - {Lk[i] * 0.6:g}*cos({th}))", f"({pz} - {Lk[i] * 0.6:g}*sin({th}))"
        layers.append({"type": "beam", "from": [fx, y, fz], "to": [ex, y, ez], "width": 0.016, "glow": 0.7, "color": c.ink})
        layers.append({"type": "mesh", "shape": "sphere", "detail": 14, "x": fx, "y": y - 0.02, "z": fz, "scale": 0.68 - 0.1 * i, "sy": 0.08, "ry": f"0 - {th}", **solid(c.col(i), 0.5), "emit": f"0.3 + 0.6*{p.hit}"})
        px, py, pz = ex, y, ez
    layers.append({"type": "mesh", "shape": "sphere", "detail": 14, "x": px, "y": py - 0.4, "z": pz, "scale": 0.2, "sy": 0.08, **solid(c.ink, 0.5)})
    layers.append({"type": "beam", "from": [px, py, pz], "to": [px, py - 0.4, pz], "width": 0.008, "glow": 0.5, "color": c.dim})
    return {"background": c.bg, "camera": cam("1.2*sin(time.bar/9)", 2.9, -6.5, look=(0, 0.9, 0), zoom=1.75), "layers": layers,
            "filters": [{"type": "shadowmap", "amount": 0.6, "soft": 3, "size": 1024, "sun": 0, "x": -2, "y": 5, "z": -6}, {"type": "tonemap", "knee": 0.8}, {"type": "aa"}, bloom(c, 0.3, 0.014, 0.8)]}


@idiom(needs=2, fam="curve", paper=True, cost=2)
def table(c):
    """A table of figures: every pair of the parts' riff lengths, one swinging a lamp across
    and the other up and down, each figure drawn by its own lamp."""
    P = []
    for p in c.riffs + c.every:
        if p.cell not in [q.cell for q in P] and p.cell <= 32:
            P.append(p)
    P = P[:3]
    if len(P) < 2:
        raise ValueError("one length")
    nn = len(P)
    sx, sy = 7.6 / nn, 4.4 / nn
    layers = []
    for i, px_ in enumerate(P):
        for j, py_ in enumerate(P):
            x0, y0 = (i - (nn - 1) / 2) * sx, ((nn - 1) / 2 - j) * sy
            x = f"{x0:g} + {0.4 * sx:g}*sin((time.beat*4 - {px_.anchor:g})/{px_.cell})"
            y = f"{y0:g} + {0.4 * sy:g}*sin((time.beat*4 - {py_.anchor:g})/{py_.cell} + 0.125)"
            L = math.lcm(px_.cell, py_.cell)
            layers.append({"type": "trail", "x": x, "y": y, "z": 0, "length": f"{min(L, 96) * 0.125 / (c.bpm / 120):g}", "samples": min(900, max(120, L * 10)), "width": 0.009, "taper": 0, "glow": 0.8, "fade": 0.6,
                           "color": c.col(i + j)})
            layers.append(ball(x, y, -0.05, 0.045, 6, **glow(c.ink, 2.5)))
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.3, 0.014, 0.6)]}


@idiom(needs=2, fam="curve", paper=True)
def epicycle(c):
    """Wheels on wheels: each arm turns once a riff at the end of the last, and the pen at
    the end of them all draws a figure that closes when they have all come round."""
    P = c.riffs[:3]
    Ls = [1.25, 0.7, 0.4]
    x, y = "0", "0"
    layers = []
    for i, p in enumerate(P):
        th = f"((time.beat*4 - {p.anchor:g})/{p.cell}*{1 if i % 2 == 0 else -1} + 0.25)"
        nx, ny = f"({x} + {Ls[i]}*cos({th}))", f"({y} + {Ls[i]}*sin({th}))"
        layers.append({"type": "beam", "from": [x, y, 0], "to": [nx, ny, 0], "width": 0.022, "glow": 0.95, "color": c.dim})
        layers.append({"type": "mesh", "shape": "torus", "detail": 48, "x": x, "y": y, "z": 0.05, "scale": Ls[i] / 0.8, "tube": 0.018 / Ls[i], "rx": 0.25, **glow(c.dim, 0.45)})
        x, y = nx, ny
    L = math.lcm(*[p.cell for p in P])
    layers.append({"type": "trail", "x": x, "y": y, "z": 0, "length": f"{min(L, 200) * 0.125 / (c.bpm / 120):g}", "samples": min(3000, max(300, L * 12)), "width": 0.026, "taper": 0, "glow": 1.45, "fade": 0.65, "color": c.a})
    layers.append(ball(x, y, -0.05, 0.085, 8, **glow(c.ink, 3.2)))
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.35, 0.016, 0.55)]}


@idiom(needs=0, drums=True, fam="field3", cost=2)
def membrane(c):
    """The drum's own skin, seen in wire: each drum throws it into a different shape."""
    D = (c.drums + c.riffs + c.parts)[:3]
    env = {f"d{i}": {"on": f"track.{p.name}", "attack": "0ms", "decay": "500ms"} for i, p in enumerate(D)}
    modes = ["cos(vtx.x*0.25)*cos(vtx.z*0.25)", "sin(vtx.x*0.5)*cos(vtx.z*0.25)", "sin(vtx.x*0.5)*sin(vtx.z*0.75)"]
    disp = " + ".join(f"0.45*env.d{i}*{modes[i]}*cos(env.d{i}.age*{3 + 2 * i})" for i in range(len(D)))
    layers = [{"type": "mesh", "shape": "plane", "detail": 46, "mode": "wire", "x": 0, "y": 0, "z": 0, "scale": 2.6, "displace": disp, "width": 1.0, **glow(c.ink, 0.9), "colour": "height", "palette": [c.b, c.ink, c.a], "spread": 1.0}]
    return {"background": c.bg, "env": env, "camera": cam("4.5*sin(time.bar/16)", 2.6, "0 - 4.5*cos(time.bar/16)", zoom=1.5), "layers": layers, "filters": [bloom(c, 0.4, 0.016, 0.5)]}


@idiom(needs=0, tune=True, fam="trace", cost=2)
def contour(c):
    """The tune as a road of light: each note a post as high as its pitch, joined to the
    next, going away into the dark."""
    T = (c.tunes + c.riffs)[0]
    y = T.pitch(0.2, 2.6)
    yn = T.pitch(0.2, 2.6, "(note.next_key*84 + 24)")
    w = "(1.5 - 1.1*note.age)"
    wn = "(1.5 - 1.1*(note.age - note.gap))"
    z = "(0.8*sin(note.beat/8))"
    zn = "(0.8*sin((note.beat + note.gap)/8))"
    N = {"track": T.name, "past": 14, "ahead": 1}
    layers = [floor(c, 0, "#12151f", 0.35), lamp(0, 3.5, -2.5, 1.15), lamp(-3, 2, -4, 0.5, c.b),
              {"type": "beam", "notes": N, "from": [w, y, z], "to": [wn, yn, zn], "width": 0.042, "glow": "1.6*exp(0 - 0.13*max(note.age, 0))", "color": c.a, "samples": 16},
              {"type": "beam", "notes": N, "from": [w, 0, z], "to": [w, y, z], "width": 0.015, "glow": "0.65*exp(0 - 0.12*max(note.age, 0))", "color": c.dim, "samples": 8},
              ball(w, y, z, "0.095*(1 + 1.5*exp(0 - 3*max(note.age, 0)))", 8, notes=N, **glow(c.ink, "1.3 + 3.0*exp(0 - 3*max(note.age, 0))"))]
    return {"background": c.bg, "camera": cam(2.5, 1.9, -6.5, look=(-1.2, 1.2, 0), zoom=1.4), "layers": layers,
            "filters": [{"type": "reflect", "y": 0, "amount": 0.4}, {"type": "tonemap", "knee": 0.7}, {"type": "aa"}, bloom(c, 0.5, 0.02, 0.55)]}


@idiom(needs=0, fam="body", cost=3)
def choir(c):
    """A choir on its risers, one singer to a part: each opens its mouth as its part sounds."""
    P = (c.tunes + c.riffs + c.drums + c.parts)
    names, Q = set(), []
    for p in P:
        if p.name not in names:
            names.add(p.name), Q.append(p)
    Q = Q[:6]
    # Up to three stand in one row; more stand in two, the back row a step up and in the gaps.
    nf = len(Q) if len(Q) <= 3 else (len(Q) + 1) // 2
    nb = len(Q) - nf
    sp, off = 1.45, (1.45 / 4 if nb == nf else 0)
    layers = [lamp(-2, 4, -6, 0.5), lamp(3, 2, -5, 0.5, c.a), lamp(0, 2.5, -4, 0.22, c.b)]
    for i, p in enumerate(Q):
        back = i >= nf
        x = ((i - nf) - (nb - 1) / 2) * sp + off if back else (i - (nf - 1) / 2) * sp - off
        y0, z0 = (-1.17, 0.95) if back else (-1.75, 0)
        layers.append({"type": "figure", "rig": "human", "motion": "sway", "energy": 0.4, "phase": i * 0.7, "x": x, "y": f"{y0} + 0.05*track.{p.name}.level", "z": z0, "scale": 2.0,
                       "mouth": f"clamp(1.6*track.{p.name}.level, 0, 1)", **skin(("#d9cdbb", "#c7b8a6")[i % 2], f"0.25*track.{p.name}.level"), "melt": 0.08,
                       "pose": {"arm_l": [0, 0, -0.02], "arm_r": [0, 0, 0.02], "head": [f"0 - 0.03 - 0.05*track.{p.name}.level", 0, 0]}})
    # From the waist up: the mouths are what move.
    look_y, zoom = (-0.58, 2.75) if nb else (-0.62, 3.0 if nf <= 2 else 2.6)
    return {"background": c.bg, "camera": cam("0.5*sin(time.bar/10)", -0.2, -6.5, look=(0, look_y, 0.3), zoom=zoom), "layers": layers, "filters": post3d(-2, 4, -6, shadow=0.4)}


# ───────────────────────── more worlds ─────────────────────────

def shots(c, look, cams, lead=None, secs=3.6):
    """Several cameras on one scene, cut where the lead riff begins a turn (so the cuts keep
    the riff's time, not the bar's), every few seconds; which camera opens goes with the variant."""
    p = lead or (c.riffs or c.drums or c.parts)[0]
    cell = p.cell or 16
    per = max(1, round(secs / c.six / cell))
    k = len(cams)
    r = c.variant % k
    look["camera"] = cams[r:] + cams[:r]
    look["shot"] = f"floor(fract(floor((time.beat*4 - {p.anchor:g})/{cell * per})/{k} + 0.001)*{k} + 0.01)"
    return look


@idiom(needs=0, fam="string", paper=True)
def slack(c):
    """A cord for each part with a weight hung on it: every note pulls the cord tight, and
    it runs slack again until the next."""
    names, P = set(), []
    for p in c.every + c.drums + c.tunes + c.parts:
        if p.name not in names:
            names.add(p.name), P.append(p)
    P = P[:6]
    env = {f"s{i}": {"on": f"track.{p.name}", "attack": "0ms", "decay": f"{max(0.25, min(2.0, (p.cell or 8) * c.six * 0.9)):.2f}"} for i, p in enumerate(P)}
    w = min(2.6, 8.4 / len(P))
    layers = []
    for i, p in enumerate(P):
        x = (i - (len(P) - 1) / 2) * w
        sag = f"(0.08 + 3.0*(1 - env.s{i}))"
        layers.append({"type": "beam", "from": [x - w * 0.42, 2.0, 0], "to": [x + w * 0.42, 2.0, 0], "width": 0.032, "glow": f"0.6 + 1.3*env.s{i}", "sag": sag, "color": c.col(i), "samples": 56})
        layers.append(box(x, f"2.0 - {sag} - 0.3", 0, 0.17, 0.28, 0.06, **glow(c.col(i), f"0.6 + 1.6*env.s{i}")))
        # How far it has run slack is read off a rule behind it.
        layers.append(box(x, 0.35, 0.2, 0.004, 1.75, 0.004, **glow(c.dim, 0.35)))
        layers.append(box(x, "2.0 - 0.38 - 0.5*inst.i", 0.2, 0.05, 0.004, 0.004, count=7, **glow(c.dim, 0.5)))
        for sx in (-1, 1):
            layers.append(box(x + sx * w * 0.42, 2.12, 0.05, 0.024, 0.19, 0.02, **glow(c.dim, 0.7)))
    return {"background": c.bg, "env": env, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.35, 0.016, 0.6)]}


@idiom(needs=0, fam="travel", cost=3)
def escalator(c):
    """A stair that comes down as fast as it is climbed: the climber keeps the music's pace
    and the top stays where it was."""
    A = (c.riffs + c.drums + c.parts)[0]
    nn = 30
    s = f"(inst.i - 15 + fract(time.beat*2))"
    layers = [{"type": "sky", "zenith": "#1c2a4a", "horizon": c.b, "ground": "#15151a", "sun": "#fff1d6", "sun_yaw": 0.28, "sun_height": 0.06, "sun_size": 0.04},
              box(f"{s}*0.42", f"{s}*0.26 - 0.13", 0, 0.21, 0.13, 0.8, count=nn, **solid("#b9b4a8", 0.8), emit=f"0.8*{A.hit}*step(abs({s}), 0.6)"),
              {"type": "mesh", "shape": "cone", "detail": 5, "x": 5.2, "y": 3.0, "z": 9, "scale": 2.6, "sy": 1.3, **solid("#4a4f63", 0.95)},
              {"type": "mesh", "shape": "cone", "detail": 5, "x": 1.5, "y": 2.2, "z": 12, "scale": 3.4, "sy": 0.9, **solid("#3d4257", 0.95)},
              {"type": "figure", "rig": "human", "motion": "walk", "x": 0.1, "y": 1.0, "z": 0, "scale": 0.82, "ry": 0.25, **skin(c.a, 0.25)}]
    look = {"background": "#1c2a4a", "layers": layers,
            "filters": [{"type": "shadowmap", "amount": 0.6, "soft": 2, "size": 1024}, {"type": "ao", "amount": 0.5, "radius": 0.05}, {"type": "atmos", "amount": 0.6, "density": 0.03, "falloff": 0.3, "shafts": 0.3},
                        {"type": "tonemap", "knee": 0.8}, {"type": "aa"}]}
    return shots(c, look, [cam(-1.2, 1.3, -6.5, look=(0.4, 1.0, 0), zoom=1.5), cam(-3.5, -0.6, -3.2, look=(0.2, 1.1, 0), zoom=1.2), cam(2.8, 3.6, -4.0, look=(0, 0.6, 0), zoom=1.4)], A)


@idiom(needs=1, fam="count", paper=True)
def tally(c):
    """A tally kept of each riff: a stroke for every note, and a line struck through them
    each time the riff comes round."""
    P = c.riffs[:3]
    u = 0.2
    layers = []
    for i, p in enumerate(P):
        y = ((len(P) - 1) / 2 - i) * 1.5
        layers.append(box("4.2 - 0.8*note.age", y, 0, 0.018, "0.42*(0.5 + 0.5*note.vel)", 0.01, notes={"track": p.name, "past": 44}, **glow(c.col(i), "0.8 + 1.5*exp(0 - 3*note.age)")))
        # The strokes through: one for each turn of the riff that is done.
        ln = math.hypot(u * p.cell * 0.9, 0.7)
        age = f"((fract({p.turn}) + inst.i + 1)*{p.cell})"         # sixteenths since that turn began
        layers.append(box(f"4.2 - {u}*({age} - {p.cell / 2:g})", y, -0.03, ln / 2, 0.012, 0.01, count=int(44 / max(p.cell / 4, 0.5)) + 1, rz=math.atan2(0.7, u * p.cell * 0.9) / math.tau, **glow(c.ink, 0.9)))
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.3, 0.014, 0.65)]}


@idiom(needs=1, fam="body", cost=3, max_cell=13)
def hands(c):
    """Two hands with as many fingers as their riffs have sixteenths; each finger comes down
    in its turn."""
    P = [p for p in c.riffs if 3 <= p.cell <= 13][:2]
    if not P:
        raise ValueError("no hand")
    layers = [lamp(-2, 4, -6, 0.65), lamp(3, 1, -5, 0.42, c.a), lamp(0, -1, -6, 0.2, c.b), floor(c, -1.9, "#16161a", 0.5)]
    for i, p in enumerate(P):
        nn = p.cell
        bones = [{"name": "wrist", "parent": None, "length": 0.45, "dir": [0, 1, 0], "width": 0.11}, {"name": "palm", "parent": "wrist", "length": 0.38, "dir": [0, 1, 0], "width": 0.15 + 0.012 * nn}]
        pose = {"wrist": [0.02, 0, f"{0.02 * (1 if i else -1)}*sin(time.bar/3)"]}
        for k in range(nn):
            fan = (k - (nn - 1) / 2) / max(nn - 1, 1) * 1.5
            ln = 0.34 - 0.1 * abs(fan) / 0.75
            bones.append({"name": f"f{k}a", "parent": "palm", "length": ln, "dir": [fan, 1, 0], "width": 0.04})
            bones.append({"name": f"f{k}b", "parent": f"f{k}a", "length": ln * 0.8, "dir": [fan, 1, 0], "width": 0.034})
            e = f"exp(0 - 1.3*fract({p.turn} - {k / nn:.5f})*{nn})"
            pose[f"f{k}a"] = [f"0.03 + 0.17*{e}", 0, 0]
            pose[f"f{k}b"] = [f"0.04 + 0.2*{e}", 0, 0]
        x = (i - (len(P) - 1) / 2) * 3.4
        layers.append({"type": "figure", "bones": bones, "motion": "none", "pose": pose, "x": x, "y": -1.8, "z": 0, "scale": 2.3, **skin(("#c4ad96", "#b09982")[i], f"0.12*{p.hit}"), "melt": 0.06})
    return {"background": c.bg, "camera": cam("0.5*sin(time.bar/9)", 0.2, -7, look=(0, -0.2, 0), zoom=2.0), "layers": layers, "filters": post3d(-2, 4, -6, shadow=0.5)}


@idiom(needs=0, fam="body", cost=3)
def echoes(c):
    """A dancer and where the dancer was: a pose kept for each sixteenth just gone."""
    A = (c.riffs + c.drums + c.parts)[0]
    layers = [lamp(-2, 5, -6, 1.0), lamp(3, 2, -5, 0.5, c.a), floor(c, 0, "#131317", 0.3)]
    for i, p in enumerate((c.riffs + c.drums + c.parts)[:2]):
        x = f"{2.2 - 0.9 * i:g}*sin({p.turn}/2 + {0.25 * i})"
        layers.append({"type": "figure", "rig": "human", "motion": "dance", "energy": 1.2, "phase": 1.5 * i, "x": x, "y": 1.05, "z": 1.2 * i, "scale": 1.0, "echo": 9, "echo_gap": round(c.six * 2, 4),
                       "color": c.col(i), "light": 1, "ambient": 0.25, "rim": 0.5, "rim_color": c.col(i + 1), "emit": f"0.25 + 0.5*{p.hit}", "thick": 1.0})
    look = {"background": c.bg, "layers": layers, "filters": [{"type": "reflect", "y": 0, "amount": 0.35}, {"type": "tonemap", "knee": 0.75}, {"type": "aa"}, bloom(c, 0.4, 0.02, 0.7)]}
    return shots(c, look, [cam(0, 1.4, -6.5, look=(0, 1.1, 0.4), zoom=1.5), cam(-3.6, 0.5, -3.6, look=(0, 1.1, 0.4), zoom=1.3)], A)


def _fib_squares(k, unit):
    """Squares of sides 1, 1, 2, 3, 5 … laid round one another: [(centre x, centre y, side)]."""
    x0, y0, x1, y1 = 0.0, 0.0, unit, unit
    out = [(unit / 2, unit / 2, unit)]
    for i in range(1, k):
        w, h = x1 - x0, y1 - y0
        d = i % 4
        if d == 1:      # right
            out.append((x1 + h / 2, y0 + h / 2, h)); x1 += h
        elif d == 2:    # above
            out.append((x0 + w / 2, y1 + w / 2, w)); y1 += w
        elif d == 3:    # left
            out.append((x0 - h / 2, y0 + h / 2, h)); x0 -= h
        else:           # below
            out.append((x0 + w / 2, y0 - w / 2, w)); y0 -= w
    return out


@idiom(needs=1, fam="grow", cost=2)
def golden(c):
    """Squares laid round one another, each as big as the two before it together; the lamp
    goes out along them a quarter turn for every turn of the riff, and the camera draws back
    as fast as it grows."""
    A = c.riffs[0]
    sq = _fib_squares(13, 0.09)
    turns = max(2.0, (c.b16 - c.a16) / A.cell)
    per = max(1, math.ceil(turns / 7))                  # riff turns to a quarter turn of the spiral
    q = f"((time.beat*4 - {c.a16:g})/{A.cell * per})"       # quarter turns done
    phi = 1.618034
    r = f"(0.16*pow({phi}, {q} + 2))"
    px, py = 0.09 * 0.7236, 0.09 * 0.2764             # the spiral's eye, near enough
    th = f"(({q} + 0.5)*0.25)"
    layers = []
    for i, (x, y, sd) in enumerate(sq):
        layers.append(box(x, y, 0, sd / 2 * 0.955, sd / 2 * 0.955, 0.01, **glow((c.a, c.b, c.c, c.dim)[i % 4], f"0.22 + 0.5*smooth({i - 3}, {i - 2}, {q})*{A.hit} + 0.25*step({i - 2.5}, {q})")))
    layers.append({"type": "trail", "x": f"{px} + {r}*cos({th})", "y": f"{py} + {r}*sin({th})", "z": -0.1, "length": f"clamp(scene.t, 0.05, 30)", "samples": 700, "width": f"0.022*{r}", "taper": 1, "glow": 1.2, "fade": 0.6,
                   "color": c.ink})
    layers.append(ball(f"{px} + {r}*cos({th})", f"{py} + {r}*sin({th})", -0.15, f"0.12*{r}", 8, **glow(c.ink, 3)))
    return {"background": c.bg, "camera": {"x": px, "y": py, "z": -9, "look_at": [px, py, 0], "zoom": f"2.2/{r}"}, "layers": layers, "filters": [bloom(c, 0.3, 0.014, 0.6)]}


@idiom(needs=1, fam="orbit", cost=2, max_cell=16)
def moons(c):
    """A row of moons, one to a sixteenth of the riff, and one lamp going round them once a
    turn: the phases run along the row."""
    P = [p for p in c.riffs if p.cell <= 16][:2]
    if not P:
        raise ValueError("too long")
    layers = [{"type": "stars", "count": 400, "speed": 0, "size": 0.8, "light": 0.4, "twinkle": 0.2, "streak": 0}]
    for i, p in enumerate(P):
        nn = p.cell
        # (A long riff alone takes two rows, so that its moons are not beads.)
        per = nn if nn <= 9 or len(P) > 1 else -(-nn // 2)
        rows = -(-nn // per)
        y = (len(P) - 1) * 1.15 - 2.3 * i
        w = min(1.0, 8.0 / per)
        th = f"(0.75 - {p.turn})"
        layers.append({"type": "light", "x": f"4.6*cos({th})", "y": y, "z": f"4.6*sin({th})", "power": 1.6, "reach": 14 if len(P) == 1 else 8, "color": ("#fff4e0", c.a)[i]})
        d = f"(fract({p.turn} - inst.i/{nn})*{nn})"
        col_, row_ = f"(inst.i - {per}*floor(inst.i/{per}))", f"floor(inst.i/{per})"
        layers.append(ball(f"({col_} - {(per - 1) / 2})*{w:g}", f"{y} + ({(rows - 1) / 2} - {row_})*{max(w * 1.25, 1.1):g}", 0, w * 0.4, 20, count=nn, **solid("#a7a39a", 0.95), emit=f"0.25*exp(0 - 1.5*{d})*{p.hit}"))
    return {"background": "#020204", "camera": FLAT, "layers": layers, "filters": [{"type": "tonemap", "knee": 0.75}, {"type": "aa"}, bloom(c, 0.3, 0.02, 0.8)]}


@idiom(needs=0, tune=True, fam="weather", cost=2)
def lanterns(c):
    """Every note of the tune is a lantern let go over the water, as far across as its
    pitch is high."""
    T = (c.tunes + c.riffs + c.parts)[0]
    x = f"({T.pitch(-3.6, 3.6)} + 0.25*sin(note.age/5 + note.beat/3))"
    layers = [{"type": "stars", "count": 500, "speed": 0, "size": 0.8, "light": 0.5, "twinkle": 0.3, "streak": 0},
              {"type": "mesh", "shape": "plane", "detail": 4, "x": 0, "y": -1.6, "z": 0, "scale": 30, "material": "pbr", "rough": 0.15, "metal": 0.3, "color": "#05080e", "rim": 0, "cull": True},
              box(x, "0 - 1.45 + 0.34*note.age", "0.2 + 2.2*hash(note.beat)", "0.3*(0.6 + note.vel)", "0.4*(0.6 + note.vel)", 0.3, notes={"track": T.name, "past": 32}, round=0.3,
                  **glow(c.a, "2.6*exp(0 - 0.055*note.age)*(0.8 + 0.2*noise(time.t*7 + note.beat))")),
              box(x, "0 - 1.45 + 0.34*note.age - 0.42*(0.6 + note.vel)", "0.2 + 2.2*hash(note.beat)", "0.1*(0.6 + note.vel)", 0.03, 0.1, notes={"track": T.name, "past": 32}, **glow("#fff2c8", "3.2*exp(0 - 0.055*note.age)"))]
    return {"background": "#020308", "camera": cam("0.4*sin(time.bar/12)", 0.3, -6, look=(0, 0.6, 1), zoom=1.3), "layers": layers,
            "filters": [{"type": "reflect", "y": -1.6, "amount": 0.6}, {"type": "tonemap", "knee": 0.75}, {"type": "aa"}, bloom(c, 0.6, 0.03, 0.5)]}


@idiom(needs=0, fam="weather")
def fountain(c):
    """A jet for each part, thrown up by its notes."""
    names, P = set(), []
    for p in c.every + c.drums + c.tunes + c.parts:
        if p.name not in names:
            names.add(p.name), P.append(p)
    P = P[:7]
    layers = [{"type": "gradient", "palette": [c.bg, c.bg, "#0b1220"], "angle": 0.25, "spread": 0.6, "res": 0.5}]
    for i, p in enumerate(P):
        x = (i - (len(P) - 1) / 2) * min(0.5, 3.0 / len(P))
        layers.append({"type": "particles", "on": f"track.{p.name}", "count": 56, "speed": f"1.85 + 0.9*track.{p.name}.vel", "spread": 0.055, "dir": 0.25, "life": 1.85, "gravity": 1.8, "drag": 0.08, "size": 0.013,
                       "x": x, "y": -0.8, "jitter": 0.015, "soft": 0.55, "hues": 0.06, "color": c.col(i), "shape": "spark"})
        layers.append({"type": "shape", "sides": 1, "radius": 0.028, "width": 0, "fill": 1, "color": c.col(i), "x": x, "y": -0.82, "glow": f"1.4 + 4.5*track.{p.name}.hit"})
    layers.append({"type": "shape", "sides": 4, "rotate": 0.125, "radius": 2.6, "width": 0, "fill": 1, "color": "#000000", "blend": "normal", "x": 0, "y": -2.68})
    return {"background": c.bg, "layers": layers, "filters": [bloom(c, 0.5, 0.02, 0.5)]}


@idiom(needs=0, tune=True, fam="weather")
def fireworks(c):
    """The tune let off over a town: each note bursts as high as its pitch."""
    T = (c.tunes + c.riffs + c.parts)[0]
    y = T.pitch(-0.05, 0.8, f"(track.{T.name}.key*84 + 24)")
    layers = [{"type": "gradient", "palette": ["#020308", "#020308", "#0c1024"], "angle": 0.25, "spread": 0.7, "res": 0.5},
              {"type": "particles", "on": f"track.{T.name}", "count": 160, "speed": 1.0, "spread": 1, "life": 1.8, "gravity": 0.3, "drag": 1.2, "size": 0.016, "x": "1.3*noise(time.beat*0.83 + 5)", "y": y,
               "jitter": 0.0, "soft": 0.5, "hues": 0.9, "palette": [c.a, c.b, c.c, c.ink], "pos": "fract(time.beat*0.37)"}]
    for q in (c.riffs + c.drums)[:2]:
        if q.name != T.name:
            layers.insert(1, {"type": "particles", "on": f"track.{q.name}", "count": 60, "speed": 0.6, "spread": 1, "life": 1.3, "gravity": 0.3, "drag": 1.3, "size": 0.01, "x": "1.5*noise(time.beat*1.31 + 9)",
                              "y": "0.25 + 0.45*noise(time.beat*0.77 + 3)", "jitter": 0.0, "soft": 0.5, "hues": 0.2, "color": c.col(layers.__len__())})
    for k in range(22):
        hgt = 0.1 + 0.28 * ((k * 37) % 11) / 11
        layers.append({"type": "shape", "sides": 4, "rotate": 0.125, "radius": 0.085 * 1.414, "width": 0, "fill": 1, "color": "#000000", "blend": "normal", "x": -1.75 + k * 0.167, "y": -1.0 + hgt - 0.085})
    layers.append({"type": "shape", "sides": 4, "rotate": 0.125, "radius": 2.6, "width": 0, "fill": 1, "color": "#000000", "blend": "normal", "x": 0, "y": -2.75})
    return {"background": "#020308", "layers": layers, "filters": [bloom(c, 0.6, 0.025, 0.45)]}


@idiom(needs=2, fam="lattice", cost=2)
def cube(c):
    """A cube in three layers, each turned a quarter by its own riff: it is a whole cube
    only where they have all just turned."""
    P = (c.riffs + c.drums)[:3]
    layers = [lamp(-3, 5, -6, 1.2), lamp(4, -2, -5, 0.5, c.b)]
    for j in range(3):
        p = P[j % len(P)]
        T = f"({p.turn})"
        th = f"((floor({T}) + smooth(0.5, 1, fract({T})))/4)"
        ix, iz = "(inst.i - 3*floor(inst.i/3) - 1)", "(floor(inst.i/3) - 1)"
        layers.append(box(f"0.98*({ix}*cos({th}) - {iz}*sin({th}))", (j - 1) * 0.98, f"0.98*({ix}*sin({th}) + {iz}*cos({th}))", 0.45, 0.45, 0.45, count=9, ry=f"0 - {th}", round=0.08,
                          **solid(c.col(j), 0.45, 0.1), emit=f"0.35*{p.hit}"))
    spin = "time.bar/24"
    return {"background": c.bg, "camera": cam(f"6.2*sin({spin})", 3.2, f"0 - 6.2*cos({spin})", zoom=1.55), "layers": layers, "filters": post3d(-3, 5, -6, shadow=0.5)}


def _laid_walk(c, segs, hit):
    """A walk laid out to fill the frame. `segs` are its legs in order, (from, to, heading,
    length), times in sixteenths and headings in turns; each leg is drawn as it is walked,
    and a lamp goes along it. Nothing is kept from frame to frame: the walk is worked out
    here, so it can be made to fit."""
    pts = [(0.0, 0.0)]
    for _, _, h, ln in segs:
        x, y = pts[-1]
        pts.append((x + ln * math.cos(2 * math.pi * h), y + ln * math.sin(2 * math.pi * h)))
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    sc = min(7.6 / max(max(xs) - min(xs), 1e-6), 4.1 / max(max(ys) - min(ys), 1e-6))
    ox, oy = -(max(xs) + min(xs)) / 2 * sc, -(max(ys) + min(ys)) / 2 * sc
    mean = sum(ln for _, _, _, ln in segs) / len(segs) * sc
    thick = max(0.016, min(0.05, 0.06 * mean))
    now = "(time.beat*4)"
    layers, px, py = [], [f"{pts[0][0] * sc + ox:g}"], [f"{pts[0][1] * sc + oy:g}"]
    for (t0, t1, h, ln), (x, y) in zip(segs, pts):
        g = f"clamp(({now} - {t0:g})/{max(t1 - t0, 1e-3):g}, 0, 1)"
        on = f"step({t0:g}, {now})"
        dx, dy = ln * sc * math.cos(2 * math.pi * h), ln * sc * math.sin(2 * math.pi * h)
        layers.append(box(f"{x * sc + ox:g} + {dx / 2:g}*{g}", f"{y * sc + oy:g} + {dy / 2:g}*{g}", 0, f"({ln * sc / 2:g}*{g} + {thick:g})*{on}", f"{thick:g}*{on}", 0.01, rz=round(h % 1, 5),
                          **glow(c.ink, f"0.5 + 1.7*exp(0 - 0.1*max({now} - {t0:g}, 0))")))
        px.append(f"{dx:g}*{g}")
        py.append(f"{dy:g}*{g}")
    layers.append(ball("var.px", "var.py", -0.05, f"{2.2 * thick:g} + 0.12*{hit}", 10, **glow(c.a, 3)))
    return {"background": c.bg, "camera": FLAT,
            "vars": {"px": {"follow": " + ".join(px), "attack": "0ms", "release": "0ms"}, "py": {"follow": " + ".join(py), "attack": "0ms", "release": "0ms"}},
            "layers": layers, "filters": [bloom(c, 0.4, 0.016, 0.6)]}


@idiom(needs=1, fam="curve")
def turtle(c):
    """A lamp that walks straight and turns a corner each time a riff comes round, right for
    one riff and left for the other; its whole walk stays drawn, and is laid out beforehand
    so that it fills the frame."""
    A = c.riffs[0]
    B = c.riffs[1] if len(c.riffs) > 1 else None
    a0, b0 = c.a16, c.b16

    def comes(p, per):
        """The sixteenths at which the riff comes round (every `per` turns) within the scene."""
        try:
            lag = float(getattr(p, "lag", None) or 0)
        except ValueError:
            lag = 0.0
        step_, first = p.cell * per, p.anchor - lag
        k = math.floor((a0 - first) / step_) + 1
        out = []
        while first + k * step_ < b0 - 0.01:
            out.append(first + k * step_)
            k += 1
        return out

    best = None
    if B:
        per = max(1, math.ceil(((b0 - a0) / A.cell + (b0 - a0) / B.cell) / 36))
        ea, eb = comes(A, per), comes(B, per)
        cuts = sorted(set([a0] + ea + eb + [b0]))
        for sign in (1, -1):
            segs = [(t0, t1, 0.25 * (sum(1 for e in ea if e <= t0) + sign * sum(1 for e in eb if e <= t0)), t1 - t0) for t0, t1 in zip(cuts, cuts[1:])]
            x = y = 0.0
            xs, ys = [0.0], [0.0]
            for _, _, h, ln in segs:
                x, y = x + ln * math.cos(2 * math.pi * h), y + ln * math.sin(2 * math.pi * h)
                xs.append(x)
                ys.append(y)
            # (the walk that opens out the most for its length: turn the second riff that way)
            spread = math.sqrt(max(max(xs) - min(xs), 0) * max(max(ys) - min(ys), 0)) / max(sum(ln for _, _, _, ln in segs), 1e-6)
            if best is None or spread > best[0]:
                best = (spread, segs)
    if best and best[0] >= 0.06 and len(best[1]) >= 3:
        return _laid_walk(c, best[1], A.hit)
    # One riff alone (or two that turn together): the sides grow as it goes, so the walk
    # winds outward (a square, a three-cornered or a five-pointed winding, by turns).
    step, g_ = ((0.25, 0.22), (1 / 3, 0.55), (0.4, 0.5), (0.2, 0.22), (1 / 6, 0.22))[c.variant % 5]
    per = max(1, math.ceil((b0 - a0) / A.cell / 22))     # a corner every so many turns: no more than a score of corners
    cuts = sorted(set([a0] + comes(A, per) + [b0]))
    segs = [(t0, t1, step * k, (t1 - t0) * (1 + g_ * k)) for k, (t0, t1) in enumerate(zip(cuts, cuts[1:]))]
    if len(segs) < 2:
        raise ValueError("the riff does not come round here")
    return _laid_walk(c, segs, A.hit)


# ───────────────────────── a fifth lot ─────────────────────────

@idiom(needs=0, fam="sign")
def sonar(c):
    """A sweep that goes round once a bar; each note is a blip where the sweep was when it
    sounded, further out the higher it is."""
    names, P = set(), []
    for p in c.riffs + c.drums + c.tunes + c.parts:
        if p.name not in names:
            names.add(p.name), P.append(p)
    P = P[:4]
    layers = []
    for r in (0.3, 0.6, 0.9):
        layers.append({"type": "shape", "sides": 0, "radius": r, "width": 0.002, "fill": 0, "color": c.dim, "opacity": 0.6})
    for k in range(16):
        a = 0.25 - k / 16
        layers.append({"type": "shape", "sides": 1, "radius": 0.008 if k % 4 else 0.014, "width": 0, "fill": 1, "color": c.dim, "x": 0.95 * math.cos(a * math.tau), "y": 0.95 * math.sin(a * math.tau)})
    for i, p in enumerate(P):
        th = f"(0.25 - fract(note.beat/4))"
        r = p.pitch(0.18 + 0.05 * i, 0.82 + 0.03 * i)
        layers.append({"type": "shape", "notes": {"track": p.name, "past": 4}, "sides": 1, "radius": "0.018 + 0.03*exp(0 - 3*note.age)", "width": 0, "fill": 1, "color": c.col(i), "opacity": "exp(0 - 0.8*note.age)",
                       "x": f"{r}*cos({th})", "y": f"{r}*sin({th})"})
    layers.append({"type": "beam", "from": [0, 0, 0], "to": ["2.4*cos(0.25 - fract(time.bar))", "2.4*sin(0.25 - fract(time.bar))", 0], "width": 0.02, "glow": 0.9, "fade": 0.2, "color": c.a, "samples": 30, "zoom": 1.6, "dist": 3.0})
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [{"type": "expose", "open": 1, "fade": f"{c.bar_s * 0.35:.2f}", "live": 1, "mode": "light"}, bloom(c, 0.4, 0.016, 0.5)]}


@idiom(needs=0, tune=True, fam="trace", paper=True)
def constellation(c):
    """The tune as a star map: each note a star, as far across as it comes in the phrase and
    as high as its pitch, with a line drawn from each to the next as it is played."""
    T = (c.tunes + c.riffs + c.parts)[0]
    x = "((fract(note.beat/16) - 0.5)*8.2)"
    xn = "((fract(note.beat/16) + note.gap/16 - 0.5)*8.2)"
    y, yn = T.pitch(-2.0, 2.0), T.pitch(-2.0, 2.0, "(note.next_key*84 + 24)")
    N = {"track": T.name, "past": 15.5}
    layers = [{"type": "stars", "count": 350, "speed": 0, "size": 0.7, "light": 0.3, "twinkle": 0.3, "streak": 0},
              {"type": "beam", "notes": N, "from": [x, y, 0], "to": [xn, yn, 0], "reach": "clamp(div(note.age, max(note.gap, 0.1)), 0, 1)", "width": 0.035, "glow": "1.4*exp(0 - 0.05*note.age)", "color": c.a, "samples": 16},
              ball(x, y, -0.05, "0.13*(0.6 + note.vel)*(1 + 2*exp(0 - 3*note.age))", 8, notes=N, **glow(c.ink, "1.5 + 3*exp(0 - 2*note.age)"))]
    return {"background": "#020308", "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.5, 0.02, 0.5)]}


@idiom(needs=0, drums=True, fam="trace", paper=True)
def seismo(c):
    """A paper going by under a needle for each drum: every stroke is a spike as tall as it
    was hard."""
    P = (c.drums + c.riffs + c.parts)[:5]
    layers = []
    for i, p in enumerate(P):
        y = ((len(P) - 1) / 2 - i) * min(1.0, 4.4 / len(P))
        layers.append(box(0, y, 0.05, 4.4, 0.004, 0.01, **glow(c.dim, 0.5)))
        layers.append({"type": "mesh", "shape": "cone", "detail": 3, "notes": {"track": p.name, "past": 8}, "x": "4.0 - 1.02*note.age", "y": f"{y:g} + 0.32*(0.4 + note.vel)", "z": 0, "scale": 1,
                       "sx": 0.07, "sy": "0.32*(0.4 + note.vel)", "sz": 0.02, **glow(c.col(i), "0.8 + 2*exp(0 - 3*note.age)")})
        layers.append(ball(4.0, y, -0.05, f"0.04 + 0.06*{p.hit}", 8, **glow(c.ink, 2)))
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.35, 0.014, 0.6)]}


@idiom(needs=0, drums=True, fam="fall", cost=2)
def shatter(c):
    """A glass ball for each drum, whole until it is struck."""
    P = (c.drums + c.riffs + c.parts)[:4]
    env = {f"k{i}": {"on": f"track.{p.name}", "attack": "0ms", "decay": "900ms"} for i, p in enumerate(P)}
    layers = [lamp(-3, 5, -6, 1.3), lamp(4, 2, -5, 0.6, c.a), floor(c, -1.3, "#121216", 0.3)]
    for i, p in enumerate(P):
        x = (i - (len(P) - 1) / 2) * 2.1
        # Keep the shatter window wide enough (up to 0.7s) and add a bright inner core
        # revealed when the outer shell bursts apart on each drum hit.
        win = max(0.38, min(0.75, (p.cell or 8) * c.six * 0.9))
        layers.append(ball(x, 0.2, 0, f"0.16 + 0.14*env.k{i}", 10, **glow("#ffffff", f"0.5 + 2.8*env.k{i}")))
        layers.append({"type": "mesh", "shape": "sphere", "detail": 10, "x": x, "y": 0.2, "z": 0, "scale": 0.74, "shatter": f"env.k{i}.age*step(env.k{i}.age, {win:.2f}) - 0.001",
                       "burst": 1.85, "drop": 2.1, "tumble": 1.9, **solid(c.col(i), 0.15, 0.3), "emit": f"0.2 + 0.6*env.k{i}"})
    return {"background": c.bg, "env": env, "camera": cam("0.8*sin(time.bar/9)", 0.6, -7, look=(0, 0, 0), zoom=1.5), "layers": layers,
            "filters": [{"type": "reflect", "y": -1.3, "amount": 0.4}, {"type": "tonemap", "knee": 0.75}, {"type": "aa"}, bloom(c, 0.4, 0.02, 0.7)]}


@idiom(needs=0, fam="travel", cost=2)
def gates(c):
    """A flight down a tunnel of hoops: every note to come is a hoop ahead, and you go
    through each as it sounds."""
    names, P = set(), []
    for p in c.riffs + c.drums + c.tunes + c.parts:
        if p.name not in names:
            names.add(p.name), P.append(p)
    P = P[:4]
    layers = []
    for i, p in enumerate(P):
        layers.append({"type": "mesh", "shape": "torus", "detail": 40, "notes": {"track": p.name, "past": 0.5, "ahead": 10}, "x": f"0.5*sin(note.beat/8 + {i})", "y": f"0.35*cos(note.beat/6 + {i})", "z": "0 - 3.2*note.age",
                       "scale": 1.0 + 0.45 * i, "tube": 0.014, "rx": 0.25, **glow(c.col(i), "0.35 + 1.0*exp(0 - 1.2*abs(note.age))")})
    layers.append({"type": "stars", "count": 300, "speed": 0.25, "size": 0.8, "light": 0.5, "twinkle": 0.2, "streak": 1.5})
    return {"background": c.bg, "camera": cam(0, 0, -0.6, look=(0, 0, 6), zoom=0.9, roll="time.bar/16"), "layers": layers, "filters": [{"type": "fog", "amount": 1.0, "density": 0.12, "color": c.bg}, {"type": "aa"}, bloom(c, 0.3, 0.014, 0.7)]}


@idiom(needs=0, fam="travel", cost=2)
def highway(c):
    """A road with a lane for each part: its notes come down the lane as far apart as they
    are in time, and each reaches the line as it sounds."""
    names, P = set(), []
    for p in c.riffs + c.drums + c.tunes + c.parts:
        if p.name not in names:
            names.add(p.name), P.append(p)
    P = P[:5]
    w = 0.7
    layers = [lamp(0, 4, -3, 1.0), floor(c, 0, "#0d0d10", 0.5), box(0, 0.02, 0, len(P) * w / 2 + 0.1, 0.012, 0.05, **glow(c.ink, 1.2))]
    layers.append(box(f"(inst.i - {len(P) / 2})*{w}", 0.01, 12, 0.01, 0.005, 13, count=len(P) + 1, **glow(c.dim, 0.5)))
    for i, p in enumerate(P):
        x = (i - (len(P) - 1) / 2) * w
        layers.append(box(x, 0.05, "0 - 2.6*note.age + 0.5*2.6*clamp(note.len, 0.1, 1)", w * 0.36, 0.04, "0.5*2.6*clamp(note.len, 0.1, 1)*0.9", notes={"track": p.name, "past": 0.6, "ahead": 9}, round=0.3,
                          **glow(c.col(i), "0.55 + 0.9*note.on")))
        layers.append(box(x, 0.03, 0, w * 0.42, 0.02, 0.1, **glow(c.col(i), f"0.3 + 1.5*{p.hit}")))
    return {"background": c.bg, "camera": cam(0, 2.3, -3.0, look=(0, 0.2, 4), zoom=1.2), "layers": layers,
            "filters": [{"type": "fog", "amount": 1.0, "density": 0.05, "color": c.bg}, {"type": "reflect", "y": 0, "amount": 0.3}, {"type": "aa"}, bloom(c, 0.25, 0.012, 0.8)]}


@idiom(needs=0, fam="paper")
def blots(c):
    """Blotting paper: every note is a drop of ink let fall on it, spreading and soaking in."""
    names, P = set(), []
    for p in c.riffs + c.drums + c.tunes + c.parts:
        if p.name not in names:
            names.add(p.name), P.append(p)
    P = P[:4]
    inks = ("#c8341d", "#1f5f8c", "#e0a41a", "#22262e")
    layers = []
    for i, p in enumerate(P):
        nn = p.cell or 16
        layers.append({"type": "shape", "notes": {"track": p.name, "past": 12}, "sides": 1, "radius": "(0.04 + 0.11*sqrt(note.age))*(0.6 + note.vel)", "width": 0, "fill": 1, "color": inks[i], "blend": "multiply",
                       "opacity": "0.75*exp(0 - 0.25*note.age)", "x": f"(({p.nstep} + 0.5)/{nn} - 0.5)*3.0 + 0.2*noise(note.beat*1.7 + {i})", "y": f"{p.pitch(-0.7, 0.7)} + 0.15*noise(note.beat*2.3 + {i + 5})"})
    return {"background": "#ece6d6", "layers": layers, "filters": [{"type": "grain", "amount": 0.05}]}


@idiom(needs=1, fam="paper", max_cell=24)
def mondrian(c):
    """A composition of rectangles: each belongs to one sixteenth of a riff and takes its
    colour as that sixteenth sounds."""
    P = c.riffs[:3]
    # Cut the frame into rectangles by a fixed sequence of splits (the same for a given scene).
    rects = [(-4.4, -2.45, 4.4, 2.45)]
    for k in range(13):
        j = max(range(len(rects)), key=lambda q: (rects[q][2] - rects[q][0]) * (rects[q][3] - rects[q][1]))
        x0, y0, x1, y1 = rects.pop(j)
        f = 0.3 + 0.4 * c.r(k)
        if (x1 - x0) > 1.3 * (y1 - y0):
            xm = x0 + (x1 - x0) * f
            rects += [(x0, y0, xm, y1), (xm, y0, x1, y1)]
        else:
            ym = y0 + (y1 - y0) * f
            rects += [(x0, y0, x1, ym), (x0, ym, x1, y1)]
    paints = ("#d6281a", "#1b4f9c", "#f2c21a", "#16171a")
    layers = [box(0, 0, 0.1, 4.5, 2.55, 0.01, **glow("#16171a", 1))]
    for k, (x0, y0, x1, y1) in enumerate(rects):
        p = P[k % len(P)]
        step = (k * 3) % p.cell
        d = f"(fract({p.turn} - {step / p.cell:.5f})*{p.cell})"
        on = f"exp(0 - 0.9*{d})"
        layers.append(box((x0 + x1) / 2, (y0 + y1) / 2, 0, (x1 - x0) / 2 - 0.035, (y1 - y0) / 2 - 0.035, 0.01, **glow("#ece6d6", 1)))
        layers.append(box((x0 + x1) / 2, (y0 + y1) / 2, -0.02, (x1 - x0) / 2 - 0.035, (y1 - y0) / 2 - 0.035, 0.01, **glow(paints[k % 4], 1), opacity=on))
    return {"background": "#16171a", "camera": FLAT, "layers": layers, "filters": [{"type": "grain", "amount": 0.04}]}


@idiom(needs=0, fam="weather", cost=3)
def grove(c):
    """A stand of trees in a wind that keeps the music's time, their leaves coming down."""
    A = (c.riffs + c.drums + c.parts)[0]
    layers = [{"type": "sky", "zenith": "#40618f", "horizon": "#e8d9c0", "ground": "#4a4a34", "sun": "#fff0d0", "sun_yaw": 0.3, "sun_height": 0.06, "clouds": 0.3}, floor(c, 0, "#5a5a3c", 0.95),
              {"type": "figure", "rig": "tree", "motion": "sway", "energy": f"0.5 + 1.5*track.{A.name}.level", "phase": "inst.i*1.3", "count": 9, "x": "(hash(inst.i)*2 - 1)*4.5", "y": 0, "z": "hash(inst.i + 7)*7 + 0.5",
               "scale": "2.2 + 1.6*hash(inst.i + 3)", "ry": "hash(inst.i + 11)", "thick": 1.3, **solid("#3b2e22", 0.9)},
              {"type": "motes", "mode": "drift", "count": 400, "w": 10, "h": 4, "d": 8, "y": 2, "z": 3.5, "fall": 0.5, "wind_x": f"0.5 + 0.8*sin({A.turn}/2)", "wobble": 0.25, "size": 0.035, "stretch": 2.2, "tumble": 1.5,
               "glow": 0.9, "twinkle": 0, "lit": 0.6, "palette": [c.a, c.c, c.b], "spread": 1}]
    return {"background": "#e8d9c0", "camera": cam("1.5*sin(time.bar/14)", 1.5, -5.5, look=(0, 2.0, 3), zoom=1.2), "layers": layers,
            "filters": [{"type": "shadowmap", "amount": 0.6, "soft": 2, "size": 1024}, {"type": "atmos", "amount": 0.7, "density": 0.04, "falloff": 0.4, "shafts": 0.6}, {"type": "tonemap", "knee": 0.8}, {"type": "aa"}]}


@idiom(needs=1, fam="body", cost=3, max_cell=14)
def anemone(c):
    """A sea creature with an arm for each sixteenth of the riff: each curls as its turn comes."""
    A = c.riffs[0]
    nn = max(3, min(A.cell, 14))
    d = f"(fract({A.turn} - inst.i/{nn})*{nn})"
    e = f"exp(0 - 0.8*{d})"
    pose = {f"t{k}": [f"0.015 + 0.012*sin(time.bar/2 + {k * 0.1:.2f} + inst.i*0.3) + {0.055 if k > 2 else 0.01}*{e}", 0, 0] for k in range(12)}
    th = f"(inst.i/{nn})"
    layers = [lamp(-2, 5, -4, 1.0, "#bfe6ff"), lamp(2, 0.5, -3, 0.6, c.a), floor(c, 0, "#0a141c", 0.7),
              ball(0, 0.15, 0, 0.75, 20, **solid(c.b, 0.6), sy=0.5, emit=f"0.2*{A.hit}"),
              {"type": "figure", "rig": "tentacle", "motion": "none", "pose": pose, "count": nn, "x": f"0.55*cos({th})", "y": 0.3, "z": f"0.55*sin({th})", "scale": 1.5, "ry": f"0.25 - {th}", "rx": 0.03,
               **skin(c.a, f"0.15 + 0.9*{e}"), "melt": 0.04},
              {"type": "motes", "mode": "drift", "count": 300, "w": 8, "h": 4, "d": 6, "y": 2, "z": 0, "fall": -0.05, "wobble": 0.2, "size": 0.012, "glow": 0.6, "twinkle": 0.5, "color": "#9fd8ff"}]
    return {"background": "#04121c", "camera": cam("5*sin(time.bar/20)", 2.6, "0 - 5*cos(time.bar/20)", look=(0, 1.2, 0), zoom=1.5), "layers": layers,
            "filters": [{"type": "fog", "amount": 0.9, "density": 0.08, "color": "#04121c"}, {"type": "ao", "amount": 0.5, "radius": 0.06}, {"type": "tonemap", "knee": 0.75}, {"type": "aa"}, bloom(c, 0.4, 0.02, 0.7)]}


@idiom(needs=1, fam="weather", cost=3, max_cell=13)
def skein(c):
    """A skein of birds, one for each sixteenth of the riff, the beat of their wings passing
    down the line."""
    A = c.riffs[0]
    nn = max(3, min(A.cell, 13))
    k = f"(inst.i - {(nn - 1) / 2})"
    layers = [{"type": "sky", "zenith": "#31456e", "horizon": c.a, "ground": "#1a1d26", "sun": "#fff0d0", "sun_yaw": 0.08, "sun_height": 0.04, "sun_size": 0.045, "clouds": 0.35, "cloud_height": 4},
              {"type": "figure", "rig": "bird", "motion": "flap", "phase": f"4*{A.turn} - time.beat - inst.i*{4 / nn:.4f}", "count": nn, "x": f"{k}*0.85", "y": f"1.0 + 0.12*sin({A.turn} - inst.i/{nn})", "z": f"abs({k})*0.9",
               "scale": 0.8, "ry": 0.03, "color": "#0c0d12", "light": 0.3, "ambient": 0.1, "rim": 0.3, "thick": 1.2}]
    return {"background": "#31456e", "camera": cam("0.6*sin(time.bar/12)", 0.4, -5.5, look=(0, 1.0, 1.5), zoom=1.3), "layers": layers, "filters": [{"type": "tonemap", "knee": 0.8}, {"type": "aa"}, bloom(c, 0.3, 0.03, 0.85)]}


@idiom(needs=0, fam="count", cost=2)
def coins(c):
    """A coin for each part, set spinning by its notes and settling between them."""
    names, P = set(), []
    for p in c.every + c.drums + c.tunes + c.parts:
        if p.name not in names:
            names.add(p.name), P.append(p)
    P = P[:5]
    env = {f"q{i}": {"on": f"track.{p.name}", "attack": "0ms", "decay": "1500ms"} for i, p in enumerate(P)}
    layers = [lamp(-2, 5, -5, 1.6), lamp(3, 2, -4, 0.9, c.a), lamp(0, 1.5, -5, 0.8), floor(c, 0, "#101014", 0.25)]
    for i, p in enumerate(P):
        x = (i - (len(P) - 1) / 2) * 1.7
        age = f"min(env.q{i}.age, 6)"
        layers.append({"type": "mesh", "shape": "cylinder", "detail": 28, "x": x, "y": f"0.62*cos(0.21*(1 - exp(0 - 0.9*{age}))) + 0.03", "z": 0, "scale": 1, "sx": 0.6, "sy": 0.03, "sz": 0.6,
                       "rx": f"0.25 - 0.21*(1 - exp(0 - 0.9*{age}))", "ry": f"5*(1 - exp(0 - 1.6*{age})) + {i * 0.2}", **solid(("#d4af37", "#c0c0c8", "#b87333")[i % 3], 0.4, 0.7), "emit": f"0.25*env.q{i}"})
    return {"background": c.bg, "env": env, "camera": cam("0.7*sin(time.bar/8)", 1.7, -6, look=(0, 0.45, 0), zoom=1.6), "layers": layers,
            "filters": [{"type": "shadowmap", "amount": 0.6, "soft": 2.5, "size": 1024, "sun": 0, "x": -2, "y": 5, "z": -5}, {"type": "reflect", "y": 0, "amount": 0.35}, {"type": "tonemap", "knee": 0.7}, {"type": "aa"},
                        bloom(c, 0.3, 0.014, 0.85)]}


@idiom(needs=2, fam="count", cost=2)
def balance(c):
    """A pair of scales with a riff in each pan: the beam goes down on the side that is
    sounding, and stands level only when both sound together."""
    A, B = c.riffs[0], c.riffs[1]
    env = {"a": {"on": f"track.{A.name}", "attack": "0ms", "decay": "450ms"}, "b": {"on": f"track.{B.name}", "attack": "0ms", "decay": "450ms"}}
    vars_ = {"tilt": {"follow": "0.05*(env.b - env.a)", "attack": "90ms", "release": "90ms"}}
    L = 2.4
    ends = [(f"{sgn}*{L}*cos(var.tilt)", f"2.6 + {sgn}*{L}*sin(var.tilt)") for sgn in ("(0 - 1)", "1")]
    layers = [lamp(-2, 5, -6, 1.2), lamp(3, 1, -5, 0.5, c.c), floor(c, 0, "#131317", 0.5),
              {"type": "mesh", "shape": "cylinder", "detail": 12, "x": 0, "y": 1.3, "z": 0.1, "scale": 1, "sx": 0.07, "sy": 1.3, "sz": 0.07, **solid("#8c7a4a", 0.35, 0.9)},
              box(0, 2.6, 0, L, 0.04, 0.05, rz="var.tilt", **solid("#b8a468", 0.3, 0.9))]
    for (x, y), p, col, e in zip(ends, (A, B), (c.a, c.b), ("env.a", "env.b")):
        layers.append({"type": "beam", "from": [x, y, 0], "to": [x, f"{y} - 1.3", 0], "width": 0.008, "glow": 0.4, "color": c.dim})
        layers.append({"type": "mesh", "shape": "cylinder", "detail": 24, "x": x, "y": f"{y} - 1.32", "z": 0, "scale": 1, "sx": 0.7, "sy": 0.03, "sz": 0.7, **solid("#b8a468", 0.3, 0.9)})
        nn = min(p.cell, 12)
        layers.append(ball(f"{x} + 0.42*cos(inst.i/{nn})", f"{y} - 1.2 + 0.25*{e}*exp(0 - 1.4*fract({p.turn} - inst.i/{nn})*{nn})", f"0.42*sin(inst.i/{nn})", 0.1, 10, count=nn, **solid(col, 0.4), emit=f"0.6*{e}"))
    return {"background": c.bg, "env": env, "vars": vars_, "camera": cam("0.8*sin(time.bar/10)", 1.9, -7, look=(0, 1.75, 0), zoom=2.3), "layers": layers, "filters": post3d(-2, 5, -6)}


# ───────────────────────── a sixth lot ─────────────────────────

def _cast(c, k, celled=False):
    """The scene's parts, riffs first, no part twice."""
    names, out = set(), []
    for p in (c.riffs + c.every + c.drums + ([] if celled else c.tunes + c.parts)):
        if p.name not in names and (p.cell or not celled):
            names.add(p.name), out.append(p)
    return out[:k]


@idiom(needs=1, fam="count", paper=True)
def tape(c):
    """Punched tape: every note is a column of holes that spells its pitch, and the tape
    runs a sixteenth a hole."""
    P = _cast(c, 2, celled=True)
    u = 0.22
    layers = []
    for i, p in enumerate(P):
        y0 = ((len(P) - 1) / 2 - i) * 2.3
        layers.append(box(0, y0, 0.1, 4.7, 0.98, 0.01, **glow("#d9d1ba", 0.8)))
        layers.append(ball(f"4.0 - (inst.i + fract(time.beat*4))*{u}", y0 - 0.08, 0, 0.035, 6, count=40, **glow(c.bg, 1)))
        v = f"floor(note.midi - {p.lo:g} + 1.5)"
        for b in range(5):
            bit = f"step(0.5, fract({v}/{2 ** (b + 1)}))"
            layers.append(ball(f"4.0 - note.age*4*{u}", y0 + (b - 2) * 0.33 + (0.09 if b >= 2 else -0.09) - 0.08, 0, f"0.1*{bit}", 8, notes={"track": p.name, "past": 10}, **glow(c.bg, 1)))
            layers.append(ball(f"4.0 - note.age*4*{u}", y0 + (b - 2) * 0.33 + (0.09 if b >= 2 else -0.09) - 0.08, -0.02, f"0.1*{bit}*exp(0 - 2.5*note.age)", 8, notes={"track": p.name, "past": 1.5}, **glow(c.col(i), 3)))
        layers.append(box(4.0, y0, -0.05, 0.012, 1.1, 0.01, **glow(c.col(i), f"0.6 + 2*{p.hit}")))
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.3, 0.014, 0.75)]}


@idiom(needs=2, fam="count")
def venn(c):
    """A circle for each riff, lit while it sounds: where they overlap is lit only when they
    sound together."""
    P = c.riffs[:3]
    env = {f"v{i}": {"on": f"track.{p.name}", "attack": "0ms", "decay": f"{max(0.2, min(0.6, c.six * 3)):.2f}"} for i, p in enumerate(P)}
    layers = []
    for i, p in enumerate(P):
        a = 0.25 + i / len(P)
        x, y = 0.36 * math.cos(a * math.tau) * (1.25 if len(P) == 2 else 1), 0.36 * math.sin(a * math.tau) - (0.08 if len(P) == 3 else 0)
        layers.append({"type": "shape", "sides": 1, "radius": 0.56, "width": 0, "fill": 1, "color": c.col(i), "blend": "screen", "opacity": f"0.1 + 0.9*env.v{i}", "x": x, "y": y})
        layers.append({"type": "shape", "sides": 0, "radius": 0.56, "width": 0.004, "fill": 0, "color": c.col(i), "x": x, "y": y})
        nn = p.cell
        d = f"(fract({p.turn} - inst.i/{nn})*{nn})"
        layers.append({"type": "shape", "sides": 1, "repeat": nn, "radius": f"0.012 + 0.02*exp(0 - 1.5*{d})", "width": 0, "fill": 1, "color": c.ink, "x": f"{x:.4f} + 0.61*sin(inst.i/{nn})", "y": f"{y:.4f} + 0.61*cos(inst.i/{nn})"})
    return {"background": c.bg, "env": env, "layers": layers, "filters": [bloom(c, 0.3, 0.02, 0.7)]}


@idiom(needs=2, fam="lattice", paper=True)
def tartan(c):
    """A cloth woven of two riffs: one's notes are its upright stripes and the other's its
    level ones, each lit as it sounds."""
    A, B = c.riffs[0], c.riffs[1]
    wa, hb = 9.1 / A.cell, 5.12 / B.cell
    xa = f"(({A.nstep} + 0.5)/{A.cell} - 0.5)*9.1"
    yb = f"(0.5 - ({B.nstep} + 0.5)/{B.cell})*5.12"
    layers = [box(xa, 0, 0.05, wa * 0.4, 2.6, 0.01, notes={"track": A.name, "past": A.cell / 4 - 0.02}, **glow(c.a, "0.3 + 1.1*exp(0 - 2.2*note.age)"), opacity=0.8),
              box(0, yb, 0, 4.6, hb * 0.4, 0.01, notes={"track": B.name, "past": B.cell / 4 - 0.02}, **glow(c.b, "0.3 + 1.1*exp(0 - 2.2*note.age)"), opacity=0.6),
              box(f"(fract({A.turn}) - 0.5)*9.1", 0, -0.05, 0.012, 2.6, 0.01, **glow(c.ink, 1.2)), box(0, f"(0.5 - fract({B.turn}))*5.12", -0.05, 4.6, 0.012, 0.01, **glow(c.ink, 1.2)),
              ball(f"(fract({A.turn}) - 0.5)*9.1", f"(0.5 - fract({B.turn}))*5.12", -0.1, f"0.07 + 0.12*{A.hit}*{B.hit}", 8, **glow(c.ink, 3))]
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.3, 0.014, 0.75)]}


@idiom(needs=1, fam="lattice")
def maze(c):
    """A sheet of slanting strokes; each turns a quarter when its sixteenth of the riff
    comes, so the maze they make is redrawn in a wave as long as the riff."""
    A = c.riffs[0]
    B = c.riffs[1] if len(c.riffs) > 1 else A
    ix, iy = "(inst.i - 16*floor(inst.i/16))", "floor(inst.i/16)"
    ph = f"fract(({ix} + 3*{iy})/{A.cell})"
    T = f"({A.turn} - {ph})"
    rz = f"0.125 + 0.25*(floor({T}) + smooth(0, 0.3, fract({T})) + floor(hash(inst.i)*2))"
    d = f"(fract({B.turn} - fract(({ix} + 5*{iy})/{B.cell}))*{B.cell})"
    layers = [box(f"({ix} - 7.5)*0.568", f"(4 - {iy})*0.568", 0, 0.4, 0.035, 0.01, count=144, rz=rz, **glow(c.ink, f"0.5 + 1.2*exp(0 - 1.5*{d})")),
              box(f"({ix} - 7.5)*0.568", f"(4 - {iy})*0.568", 0.05, 0.27, 0.27, 0.01, count=144, **glow(c.a, f"0.5*exp(0 - 2*fract({T})*{A.cell})"))]
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.3, 0.014, 0.7)]}


@idiom(needs=1, fam="body", cost=3)
def swings(c):
    """Swings, one to a riff, each going over and back once in its turn."""
    P = c.riffs[:3]
    L, top = 2.5, 3.3
    layers = [{"type": "sky", "zenith": "#27406b", "horizon": c.b, "ground": "#2a2a22", "sun": "#ffe9c4", "sun_yaw": 0.62, "sun_height": 0.07, "sun_size": 0.04, "clouds": 0.2}, floor(c, 0, "#4a463a", 0.95),
              box(0, top, 0, len(P) * 1.0 + 0.5, 0.05, 0.05, **solid("#3a3f4a", 0.5, 0.6))]
    for sx in (-1, 1):
        layers.append(box(sx * (len(P) * 1.0 + 0.45), top / 2, 0, 0.05, top / 2, 0.05, rz=0, **solid("#3a3f4a", 0.5, 0.6)))
    for i, p in enumerate(P):
        x = (i - (len(P) - 1) / 2) * 1.9
        th = f"(0.12*sin({p.turn}))"
        sy, sz = f"({top} - {L}*cos({th}))", f"({L}*sin({th}))"
        for dx in (-0.25, 0.25):
            layers.append({"type": "beam", "from": [x + dx, top, 0], "to": [x + dx, sy, sz], "width": 0.012, "glow": 0.35, "color": "#c9c2b0", "samples": 4})
        layers.append(box(x, sy, sz, 0.32, 0.025, 0.12, rx=f"0 - {th}", **solid("#6b4a2e", 0.7)))
        layers.append({"type": "figure", "rig": "human", "motion": "none", "x": x, "y": f"{sy} + 0.1", "z": sz, "scale": 0.9, "rx": f"0 - {th}", **skin(c.col(i), 0.2),
                       "pose": {"thigh_l": [0.22, 0, 0], "thigh_r": [0.22, 0, 0], "shin_l": [f"0 - 0.16 - 0.07*sin({p.turn} + 0.2)", 0, 0], "shin_r": [f"0 - 0.16 - 0.07*sin({p.turn} + 0.2)", 0, 0],
                                "arm_l": [0.2, 0, -0.04], "arm_r": [0.2, 0, 0.04], "forearm_l": [0.2, 0, 0], "forearm_r": [0.2, 0, 0], "spine": [f"0.03*sin({p.turn} + 0.25)", 0, 0]}})
    look = {"background": "#27406b", "layers": layers,
            "filters": [{"type": "shadowmap", "amount": 0.6, "soft": 2, "size": 1024}, {"type": "ao", "amount": 0.4, "radius": 0.05}, {"type": "tonemap", "knee": 0.8}, {"type": "aa"}]}
    return shots(c, look, [cam(6.5, 1.8, -8.0, look=(0, 1.7, 0), zoom=1.5), cam(0, 1.2, -8.5, look=(0, 1.8, 0), zoom=2.0), cam(-7.5, 1.0, -1.5, look=(0, 1.8, 0), zoom=1.6)], P[0])


@idiom(needs=2, fam="body", cost=3)
def ropes(c):
    """Two ropes turned against each other, one a turn to each riff; whoever is between them
    has to clear both."""
    A, B = c.riffs[0], c.riffs[1]
    layers = [lamp(-2, 5, -6, 1.5), lamp(3, 2, -5, 0.9, c.c), floor(c, 0, "#24242c", 0.6)]
    u = "(inst.i/39)"
    for i, (p, sgn) in enumerate(((A, "1"), (B, "(0 - 1)"))):
        th = f"({sgn}*{p.turn} + {0.5 * i})"
        r = f"(1.35*sin({u}/2))"
        layers.append(ball(f"(0 - 2.5 + 5*{u})", f"1.45 + {r}*cos({th})", f"{r}*sin({th})", 0.045, 6, count=40, **glow(c.col(i), 1.3)))
    jump = f"0.55*max(pow(0.5 - 0.5*cos({A.turn}), 6), pow(0.5 - 0.5*cos({B.turn}), 6))"
    for sx in (-1, 1):
        layers.append({"type": "figure", "rig": "human", "motion": "none", "x": sx * 2.75, "y": 1.05, "z": 0, "scale": 1.0, "ry": 0.25 * sx, **skin("#8f8a80", 0.03),
                       "pose": {"arm_r": [f"0.14 + 0.05*sin({A.turn})", 0, 0.05], "arm_l": [f"0.14 + 0.05*sin({B.turn})", 0, -0.05], "forearm_r": [0.1, 0, 0], "forearm_l": [0.1, 0, 0]}})
    layers.append({"type": "figure", "rig": "human", "motion": "none", "x": 0, "y": f"1.0 + {jump}", "z": 0, "scale": 0.95, **skin(c.c, 0.25),
                   "pose": {"thigh_l": [f"0.3*{jump}", 0, 0], "thigh_r": [f"0.3*{jump}", 0, 0], "shin_l": [f"0 - 0.5*{jump}", 0, 0], "shin_r": [f"0 - 0.5*{jump}", 0, 0], "arm_l": [0, 0, -0.06], "arm_r": [0, 0, 0.06]}})
    look = {"background": c.bg, "layers": layers, "filters": post3d(-2, 5, -6, shadow=0.5)}
    return shots(c, look, [cam(0, 1.6, -7.2, look=(0, 1.4, 0), zoom=1.5), cam(-5.5, 2.2, -3.5, look=(0, 1.3, 0), zoom=1.5)], A)


@idiom(needs=1, fam="engine", cost=3, max_cell=14)
def galley(c):
    """A boat with an oar for each sixteenth of a riff on either side; the stroke runs down
    each side once a turn, and the two sides keep different riffs."""
    A = c.riffs[0]
    B = c.riffs[1] if len(c.riffs) > 1 and c.riffs[1].cell <= 14 else A
    layers = [lamp(-3, 6, -4, 1.55), lamp(3, 2, 4, 0.75, c.a), lamp(0, 4, -5, 0.45, c.b),
              {"type": "mesh", "shape": "plane", "detail": 60, "x": 0, "y": 0, "z": 0, "scale": 30, "material": "pbr", "rough": 0.22, "metal": 0.18, "color": "#0d2230", "rim": 0, "cull": True,
               "displace": "0.005*sin(vtx.x*9 + vtx.z*5 + time.t*0.4)"},
              box(0, 0.16, 0, 3.0, 0.16, 0.42, round=0.5, **solid("#6e4b30", 0.65)), box(0, 0.3, 0, 2.8, 0.03, 0.34, **solid("#3d2b1e", 0.85))]
    for p, side, col in ((A, -1, c.a), (B, 1, c.b)):
        nn = max(3, min(p.cell, 14))
        ph = f"({p.turn} - inst.i/{nn})"
        sweep = f"(0.06*sin({ph}))"
        dip = f"(0.035 + 0.03*cos({ph}))"
        x = f"((inst.i - {(nn - 1) / 2})*{5.2 / nn:g})"
        layers.append(box(x, 0.36, side * 1.25, 0.036, 0.036, 0.98, count=nn, ry=f"{side}*{sweep}", rx=f"{side}*{dip}", **solid("#dfd0b4", 0.6), emit=f"0.12 + 0.5*exp(0 - 1.2*fract({ph})*{nn})"))
        layers.append(ball(x, 0.52, side * 0.3, 0.14, 8, count=nn, **solid(col, 0.55), emit=f"0.35 + 0.8*exp(0 - 1.2*fract({ph})*{nn})"))
    layers.append({"type": "motes", "mode": "drift", "count": 200, "w": 14, "h": 0.02, "d": 8, "y": 0.02, "z": 0, "fall": 0, "wind_x": -1.6, "wobble": 0, "size": 0.02, "stretch": 6, "glow": 0.55, "twinkle": 0, "color": "#9fd0e6"})
    look = {"background": "#08121a", "layers": layers, "filters": [{"type": "shadowmap", "amount": 0.5, "soft": 2, "size": 1024, "sun": 0, "x": -3, "y": 6, "z": -4}, {"type": "tonemap", "knee": 0.75}, {"type": "aa"}, bloom(c, 0.3, 0.016, 0.8)]}
    return shots(c, look, [cam(0.01, 8.5, -0.5, look=(0, 0, 0), zoom=1.7), cam(-5.5, 2.4, -4.5, look=(0, 0.3, 0), zoom=1.6), cam(6.5, 1.0, 0.01, look=(0, 0.4, 0), zoom=1.3)], A)


@idiom(needs=1, fam="swing", cost=2, max_cell=11)
def cradle(c):
    """A row of hanging balls, one to a sixteenth: the end ones go out in turn, and strike as
    the riff comes round and again half way."""
    P = [p for p in c.riffs if p.cell <= 11][:2]
    if not P:
        raise ValueError("too long")
    top, L = 3.0, 2.0
    layers = [lamp(-3, 5, -6, 1.5), lamp(3, 1.5, -5, 0.85, c.a), floor(c, 0, "#1c1d24", 0.3)]
    for i, p in enumerate(P):
        nn = max(3, p.cell)
        r = min(0.34, 0.21 * (1 + (11 - nn) / 8 * 0.6))      # (a short riff's few balls are bigger)
        z = 1.6 * i
        x0 = (nn - 1) * r
        s = f"sin({p.turn})"
        thL, thR = f"(0 - 0.11*max({s}, 0))", f"(0.11*max(0 - {s}, 0))"
        layers.append(box(0, top, z, x0 + 0.5, 0.035, 0.035, **solid("#727782", 0.35, 0.85), emit=0.12))
        layers.append(ball(f"(inst.i + 1 - {(nn - 1) / 2})*{2 * r}", top - L, z, r, 14, count=nn - 2, **solid(c.col(i), 0.2, 0.9), emit=f"0.32 + 0.35*{p.hit}"))
        layers.append(box(f"(inst.i + 1 - {(nn - 1) / 2})*{2 * r}", top - L / 2, z, 0.005, L / 2, 0.005, count=nn - 2, **glow(c.dim, 0.75)))
        for sx, th in ((-1, thL), (1, thR)):
            bx, by = f"({sx * x0} + {L}*sin({th}))", f"({top} - {L}*cos({th}))"
            layers.append(ball(bx, by, z, r, 14, **solid(c.col(i), 0.2, 0.9), emit=f"0.35 + 0.45*{p.hit}"))
            layers.append({"type": "beam", "from": [sx * x0, top, z], "to": [bx, by, z], "width": 0.009, "glow": 0.55, "color": c.dim, "samples": 4})
    return {"background": c.bg, "camera": cam("1.2*sin(time.bar/9)", 1.9, -6.5, look=(0, 1.75, 0.5), zoom=2.3), "layers": layers,
            "filters": [{"type": "shadowmap", "amount": 0.5, "soft": 2, "size": 1024, "sun": 0, "x": -3, "y": 5, "z": -6}, {"type": "reflect", "y": 0, "amount": 0.35}, {"type": "tonemap", "knee": 0.75}, {"type": "aa"},
                        bloom(c, 0.3, 0.016, 0.8)]}


@idiom(needs=0, drums=True, fam="weather", cost=2)
def storm(c):
    """Weather: lightning on the heaviest drum, the sky lit by the next."""
    D = (c.drums + c.riffs + c.parts)[:2]
    k, sn = D[0], D[-1]
    env = {"k": {"on": f"track.{k.name}", "attack": "0ms", "decay": "320ms"}, "s": {"on": f"track.{sn.name}", "attack": "0ms", "decay": "500ms"}}
    cnt = f"track.{k.name}.count"
    x = f"(3.6*noise({cnt}*7.31 + 2))"
    layers = [{"type": "gradient", "palette": ["#04050a", "#0a0e1c", "#161c30"], "angle": 0.25, "spread": 0.8, "res": 0.5},
              {"type": "gradient", "palette": ["#000000", "#5a6a9a", "#c9d4ff"], "angle": 0.25, "spread": 0.7, "res": 0.5, "blend": "add", "opacity": "0.35*env.s + 0.5*env.k"},
              {"type": "beam", "from": [x, 2.7, 0], "to": [f"{x} + 1.4*noise({cnt}*3.17)", -1.25, 0], "width": 0.048, "taper": 0.45, "glow": "5*env.k", "jag": 0.34, "bolt": f"{cnt}*3.1 + floor(time.t*12)", "color": "#e6ecff",
               "samples": 56},
              {"type": "beam", "from": [f"{x} + 0.35*noise({cnt}*3.17)", 1.15, 0], "to": [f"{x} + 1.8*noise({cnt}*5.9)", -0.35, 0], "width": 0.018, "taper": 0.75, "glow": "2.8*env.k", "jag": 0.28, "bolt": f"{cnt}*7.3 + floor(time.t*12)",
               "color": "#c9dcff", "samples": 32},
              {"type": "motes", "mode": "drift", "count": 700, "w": 10, "h": 6, "d": 4, "y": 0, "z": 1, "fall": 7, "wind_x": -1.5, "wobble": 0, "size": 0.006, "glow": "0.3 + 0.7*env.k", "twinkle": 0,
               "color": "#aab8d8"},
              box(0, -2.0, -0.3, 6, 0.8, 0.1, color="#020203", light=0, ambient=0, rim=0),
              {"type": "figure", "rig": "tree", "motion": "sway", "energy": 1.4, "x": -2.2, "y": -1.25, "z": -0.3, "scale": 1.5, "color": "#020203", "light": 0, "ambient": 0, "rim": 0}]
    return {"background": "#04050a", "env": env, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.6, 0.03, 0.5)]}


@idiom(needs=0, fam="weather", cost=2)
def aurora(c):
    """Curtains of light over a still lake, drawn along by the tune."""
    T = (c.tunes + c.riffs + c.parts)[0]
    vars_ = {"k": {"follow": f"track.{T.name}.key", "attack": "400ms", "release": "900ms"}}
    layers = [{"type": "stars", "count": 600, "speed": 0, "size": 0.8, "light": 0.6, "twinkle": 0.3, "streak": 0}]
    for j, col in enumerate((c.a, c.b)):
        hgt = f"(1.05 + 1.35*fbm(inst.i*0.05 + {j * 9}, time.t*0.24 + var.k*2.5, {j}))"
        layers.append(box(f"(inst.i - 60)*0.2 + 1.1*sin(time.t*0.08 + inst.i*0.006 + {j * 0.3})", f"0.9 + {hgt} + 0.6*sin(inst.i*0.012 + time.t*0.1 + {j * 0.2})", 3.0 + 2 * j, 0.11, hgt, 0.01, count=120,
                          **glow(col, f"0.32 + 0.36*{hgt} + 0.75*track.{T.name}.level"), opacity=0.56))
    layers.append(box(0, -0.25, 0.5, 12, 0.3, 0.1, color="#010102", light=0, ambient=0, rim=0))
    layers.append({"type": "mesh", "shape": "cone", "detail": 4, "x": -2.6, "y": 0.25, "z": 0.4, "scale": 1.4, "sy": 0.5, "color": "#010102", "light": 0, "ambient": 0, "rim": 0})
    layers.append({"type": "mesh", "shape": "cone", "detail": 4, "x": 3.0, "y": 0.2, "z": 0.4, "scale": 1.9, "sy": 0.4, "color": "#010102", "light": 0, "ambient": 0, "rim": 0})
    return {"background": "#010206", "vars": vars_, "camera": cam(0, 0.5, -7, look=(0, 0.6, 0), zoom=1.3), "layers": layers,
            "filters": [{"type": "reflect", "y": -0.05, "amount": 0.55}, {"type": "blur", "radius": 0.004}, bloom(c, 0.6, 0.04, 0.35)]}


@idiom(needs=2, fam="travel", cost=2)
def crossing(c):
    """Two roads cross: every note is a car, and reaches the crossing as it sounds. The
    riffs' cars go through each other's gaps until they meet."""
    A, B = c.riffs[0], c.riffs[1]
    v = 2.4
    layers = [lamp(0, 6, 0, 1.3), lamp(-5, 3, -5, 0.7, c.c), floor(c, 0, "#16161c", 0.7), box(0, 0.01, 0, 12, 0.005, 0.5, **solid("#34343e", 0.9)), box(0, 0.011, 0, 0.5, 0.005, 12, **solid("#34343e", 0.9)),
              {"type": "light", "x": 0, "y": 0.6, "z": 0, "power": f"0.3 + 2.5*{A.hit}*{B.hit}", "reach": 5, "color": "#ffffff"},
              box(f"{v}*note.age", 0.1, 0.12, 0.2, 0.07, 0.1, notes={"track": A.name, "past": 4, "ahead": 4}, round=0.3, **glow(c.a, "0.7 + 2*exp(0 - 6*abs(note.age))")),
              box(-0.12, 0.1, f"0 - {v}*note.age", 0.1, 0.07, 0.2, notes={"track": B.name, "past": 4, "ahead": 4}, round=0.3, **glow(c.b, "0.7 + 2*exp(0 - 6*abs(note.age))"))]
    look = {"background": c.bg, "layers": layers, "filters": [{"type": "reflect", "y": 0, "amount": 0.3}, {"type": "aa"}, bloom(c, 0.5, 0.02, 0.6)]}
    return shots(c, look, [cam(-4.5, 5.5, -4.5, look=(0, 0, 0), zoom=1.4), cam(0.01, 9, -0.3, look=(0, 0, 0), zoom=1.5), cam(-6, 0.7, -1.2, look=(0, 0.2, 0), zoom=1.2)], A)


@idiom(needs=0, drums=True, fam="engine", cost=2)
def press(c):
    """A belt for each part bringing its notes to a press, which comes down on each as it
    sounds."""
    P = _cast(c, 2)
    env = {f"p{i}": {"on": f"track.{p.name}", "attack": "0ms", "decay": "170ms"} for i, p in enumerate(P)}
    layers = [lamp(-3, 5, -6, 1.8), lamp(3, 2, -5, 1.0, c.a), lamp(0, 3, 5, 0.8, c.b), floor(c, 0, "#20202a", 0.6)]
    for i, p in enumerate(P):
        z = 1.7 * i
        layers.append(box(0, 0.35, z, 5.5, 0.05, 0.42, **solid("#454854", 0.6, 0.5)))
        layers.append({"type": "mesh", "shape": "cylinder", "detail": 10, "count": 16, "x": "(inst.i - 7.5)*0.7", "y": 0.25, "z": z, "scale": 1, "sx": 0.09, "sy": 0.42, "sz": 0.09, "rx": 0.25, "ry": 0,
                       "rz": "time.beat*0.5", **solid("#7d818c", 0.4, 0.8)})
        done = "step(0, note.age)"
        layers.append(box("0 - 1.5*note.age", f"0.4 + 0.17*(1 - 0.75*{done})", z, 0.17, f"0.17*(1 - 0.75*{done})", 0.17, notes={"track": p.name, "past": 4, "ahead": 4}, round=0.2,
                          **solid(c.col(i), 0.5), emit=f"0.2 + 1.2*exp(0 - 5*abs(note.age))"))
        layers.append(box(0, f"1.5 - 0.92*env.p{i}", z, 0.34, 0.4, 0.34, **solid("#b4b8c2", 0.3, 0.9)))
        layers.append(box(0, 2.3, z, 0.12, 0.6, 0.12, **solid("#7d818c", 0.4, 0.8)))
        layers.append(box(0, 2.9, z, 0.7, 0.08, 0.5, **solid("#5a5e68", 0.5, 0.6)))
    look = {"background": c.bg, "env": env, "layers": layers, "filters": post3d(-3, 5, -6, shadow=0.6)}
    return shots(c, look, [cam("1.0*sin(time.bar/8)", 2.2, -6.5, look=(0, 1.0, 0.6), zoom=1.5), cam(4.5, 1.3, -3.2, look=(0, 0.9, 0.6), zoom=1.5), cam(-2.2, 3.4, -3.0, look=(0, 0.6, 0.5), zoom=1.5)], P[0])


@idiom(needs=1, fam="plate3", cost=3, max_cell=13)
def zoetrope(c):
    """A turning ring of walkers, one for each sixteenth of the riff, each a step further on
    than the last, lit only on the sixteenths: the ring stands still and one walker walks."""
    A = c.riffs[0]
    nn = max(5, min(A.cell, 13))
    R = 2.3
    th = f"(inst.i/{nn} - (time.beat*4 - {A.anchor:g})/{nn})"
    layers = [lamp(0, 4.5, 0, 1.3, "#fff0d0", 9), lamp(0, 2, -6, 0.5), floor(c, 0, "#141418", 0.4),
              {"type": "mesh", "shape": "cylinder", "detail": 40, "x": 0, "y": 0.05, "z": 0, "scale": 1, "sx": R + 0.5, "sy": 0.05, "sz": R + 0.5, **solid("#2a2428", 0.6)},
              {"type": "mesh", "shape": "cylinder", "detail": 12, "x": 0, "y": 1.6, "z": 0, "scale": 1, "sx": 0.08, "sy": 1.6, "sz": 0.08, **solid("#8c7a4a", 0.35, 0.9)},
              {"type": "figure", "rig": "human", "motion": "walk", "phase": f"inst.i*{2 / nn:.4f} - time.beat", "count": nn, "x": f"{R}*sin({th})", "y": 1.1, "z": f"0 - {R}*cos({th})", "scale": 1.0, "ry": f"0.25 - {th}",
               **skin(c.a, 0.15)}]
    return {"background": c.bg, "camera": cam(0, 1.9, -7.2, look=(0, 1.1, 0), zoom=1.5), "layers": layers,
            "filters": [{"type": "shadowmap", "amount": 0.5, "soft": 2, "size": 1024, "sun": 0, "x": 0, "y": 4.5, "z": -0.5}, {"type": "tonemap", "knee": 0.8}, {"type": "aa"},
                        {"type": "step", "every": 0.25, "live": 0.12}, bloom(c, 0.3, 0.016, 0.8)]}


@idiom(needs=1, fam="sign", max_cell=13)
def numerals(c):
    """Each riff counted aloud in figures."""
    P = [p for p in c.riffs if p.cell <= 13][:2]
    if not P:
        raise ValueError("too long to count")
    layers = []
    for i, p in enumerate(P):
        x = (i - (len(P) - 1) / 2) * 1.7
        for k in range(p.cell):
            d = f"(fract({p.turn} - {k / p.cell:.5f})*{p.cell})"
            layers.append({"type": "text", "text": str(k + 1), "size": f"0.95*(1 + 0.12*exp(0 - 4*{d}))", "x": x, "y": -0.45, "align": "center", "width": 0.22, "skew": 0, "color": c.col(i) if k else c.ink,
                           "opacity": f"step({d}, 0.999)"})
        nn = p.cell
        d2 = f"(fract({p.turn} - inst.i/{nn})*{nn})"
        layers.append({"type": "shape", "sides": 1, "repeat": nn, "radius": f"0.012 + 0.012*step({d2}, 0.999)", "width": 0, "fill": 1, "color": c.col(i), "opacity": f"0.3 + 0.7*step({d2}, 0.999)",
                       "x": f"{x:g} + (inst.i - {(nn - 1) / 2})*0.07", "y": -0.82})
    return {"background": c.bg, "layers": layers, "filters": [bloom(c, 0.3, 0.014, 0.7)]}


@idiom(needs=1, fam="orbit", cost=2)
def globe(c):
    """A world that turns once for each turn of the riff; every note is a light on it, at
    the meridian as it sounds."""
    A = c.riffs[0]
    B = c.riffs[1] if len(c.riffs) > 1 else None
    R = 1.9
    layers = [{"type": "stars", "count": 400, "speed": 0, "size": 0.8, "light": 0.4, "twinkle": 0.2, "streak": 0}, lamp(-5, 3, -6, 0.9, "#bcd0ff"),
              ball(0, 0, 0, R * 0.95, 24, **solid("#192a4c", 0.72), emit=0.06),
              {"type": "mesh", "shape": "sphere", "detail": 18, "mode": "wire", "x": 0, "y": 0, "z": 0, "scale": R, "ry": f"0 - {A.turn}", "color": c.ink, "emit": 0.95, "light": 0, "ambient": 0, "rim": 0, "width": 1.4}]
    for i, (p, rr) in enumerate(((A, R * 1.01), (B, R * 1.22))):
        if not p:
            continue
        lon = f"({p.nph} - fract({p.turn}))"
        lat = p.pitch(-0.16, 0.16)
        layers.append(ball(f"{rr}*cos({lat})*sin({lon})", f"{rr}*sin({lat})", f"0 - {rr}*cos({lat})*cos({lon})", "0.075 + 0.1*exp(0 - 2*note.age)", 8, notes={"track": p.name, "past": max(4, p.cell / 4 * 2)},
                          **glow(c.col(i), "0.8 + 3*exp(0 - 1.5*note.age)")))
    return {"background": "#020205", "camera": cam("0.6*sin(time.bar/11)", 0.8, -7, zoom=1.6), "layers": layers, "filters": [{"type": "aa"}, bloom(c, 0.5, 0.02, 0.55)]}


@idiom(needs=0, fam="trace", tune=True)
def metro(c):
    """A railway map drawn as it is played: each part a line, each note a station, the line
    running level and then slanting to the next pitch."""
    P = _cast(c, 2)
    layers = []
    for i, p in enumerate(P):
        lane = lambda src: f"((floor({p.pitch(0, 4.99, src)}) - 2)*0.8 + {(i - 0.5) * 0.3:g})"
        v = min(1.3, 0.45 / max(c.six, 0.05) / 4)             # a sixteenth is 0.45 wide at most
        x, xn = f"(3.9 - {v:g}*note.age)", f"(3.9 - {v:g}*(note.age - note.gap))"
        y, yn = lane("note.midi"), lane("(note.next_key*84 + 24)")
        N = {"track": p.name, "past": 8.5 / v}
        bend = f"({xn} - min(0.3, {v / 2:g}*note.gap))"
        go = "clamp(div(note.age, max(note.gap, 0.05)), 0, 1)"
        layers.append({"type": "beam", "notes": N, "from": [x, y, 0.02 * i], "to": [bend, y, 0.02 * i], "reach": f"clamp({go}*1.4, 0, 1)", "width": 0.06, "glow": 0.9, "fade": 0, "color": c.col(i), "samples": 6})
        layers.append({"type": "beam", "notes": N, "from": [bend, y, 0.02 * i], "to": [xn, yn, 0.02 * i], "reach": f"clamp(({go} - 0.7)*3.4, 0, 1)", "width": 0.06, "glow": 0.9, "fade": 0, "color": c.col(i), "samples": 6})
        layers.append(ball(x, y, -0.05, 0.1, 10, notes=N, **glow(c.ink, 1.1)))
        layers.append(ball(x, y, -0.1, 0.06, 10, notes=N, **glow(c.bg, 1)))
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.25, 0.012, 0.8)]}


# ───────────────────────── a seventh lot ─────────────────────────

@idiom(needs=0, fam="fall", cost=2)
def galton(c):
    """A board of pegs: every note is a ball let fall through it, going left or right at
    each peg."""
    P = _cast(c, 2)
    rows, dx, dy = 8, 0.86, 0.54
    rate = 1.0 / max(c.six * 4 * 2.2, 0.25)                # rows a beat: a ball is 2.2 s on the board
    layers = []
    for r in range(rows):
        layers.append(ball(f"(inst.i - {r / 2})*{dx}", 2.1 - r * dy, 0.05, 0.06, 6, count=r + 1, **glow(c.dim, 1.2)))
    for i, p in enumerate(P):
        row = f"(note.age*{rate:g})"
        x = " + ".join(f"smooth({r}, {r + 0.6}, {row})*(step(0.5, hash(note.beat*7.13 + {r + 3 * i})) - 0.5)" for r in range(rows))
        y = f"2.35 - {dy}*(floor({row}) + pow(fract({row}), 2)) + 0.12*sin(fract({row})/2)"
        layers.append(ball(f"({x})*{dx}", y, 0, "0.15*(0.6 + note.vel)", 8, notes={"track": p.name, "past": (rows + 0.6) / rate}, **glow(c.col(i), "1 + 2*exp(0 - 3*note.age)")))
    layers.append(box(f"(inst.i - {rows / 2})*{dx}", 2.1 - rows * dy - 0.15, 0.05, 0.015, 0.25, 0.01, count=rows + 1, **glow(c.dim, 1.0)))
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.4, 0.016, 0.6)]}


@idiom(needs=1, fam="engine", cost=2)
def musicbox(c):
    """A music box: a drum for each riff, as far round as the riff is long, with a pin for
    every note; the pins come under the comb as they sound."""
    P = c.riffs[:2]
    big = max(p.cell for p in P)
    layers = [lamp(-3, 5, -6, 1.5), lamp(3, 1, -5, 0.7, c.a), floor(c, -1.6, "#1d1d24", 0.5)]
    for i, p in enumerate(P):
        R = 1.25 * p.cell / big
        y0 = -1.5 + R + 0.02
        x0 = (i - (len(P) - 1) / 2) * 4.2
        ang = f"({p.nph} - fract({p.turn}))"                 # the pin's place round the drum: at the comb (the top, nearest us) as it sounds
        px = f"{x0:g} + {p.pitch(-1.3, 1.3)}"
        layers.append({"type": "mesh", "shape": "cylinder", "detail": 40, "x": x0, "y": y0, "z": 0, "scale": 1, "sx": R, "sy": 1.5, "sz": R, "rz": 0.25, **solid("#8f7436", 0.5, 0.4)})
        layers.append(ball(px, f"{y0:g} + {R * 1.04:g}*cos({ang})", f"0 - {R * 1.04:g}*sin({ang})", 0.12, 8, notes={"track": p.name, "past": p.cell / 4 - 0.05}, **glow("#fff3cf", "1.1 + 2.5*exp(0 - 4*note.age)")))
        layers.append(box(f"{x0:g} + (inst.i - 11.5)*0.113", y0 + R + 0.12, -0.5, 0.045, 0.012, 0.5, count=24, **solid("#c9cdd4", 0.25, 0.9)))
        layers.append(box(px, y0 + R + 0.14, -0.5, 0.05, 0.012, 0.5, notes={"track": p.name, "past": 0.5}, **glow(c.col(i), "3*exp(0 - 5*note.age)")))
    look = {"background": c.bg, "layers": layers, "filters": post3d(-3, 5, -6, shadow=0.6)}
    wide = 1.9 if len(P) == 1 else 1.45
    return shots(c, look, [cam("1.0*sin(time.bar/9)", 1.4, -6.0, look=(0, -0.4, 0), zoom=wide), cam(-5.0, 0.6, -2.5, look=(0, -0.4, 0), zoom=wide * 0.9), cam(0, 5.0, -2.5, look=(0, -0.3, 0), zoom=wide)], P[0])


@idiom(needs=0, drums=True, fam="body", cost=3)
def kit(c):
    """Somebody at a kit: an arm for the snare, an arm for the cymbal, a foot for the kick."""
    k, sn, hh = c.kick or (c.drums + c.parts)[0], c.snare or (c.drums + c.parts)[-1], c.hat or (c.drums + c.parts)[0]
    env = {"k": {"on": f"track.{k.name}", "attack": "0ms", "decay": "200ms"}, "s": {"on": f"track.{sn.name}", "attack": "0ms", "decay": "200ms"}, "h": {"on": f"track.{hh.name}", "attack": "0ms", "decay": "160ms"}}
    drum = lambda x, y, z, r, h, col, e: {"type": "mesh", "shape": "cylinder", "detail": 24, "x": x, "y": y, "z": z, "scale": 1, "sx": r, "sy": h, "sz": r, **solid(col, 0.4, 0.3), "emit": e}
    layers = [lamp(-2, 5, -6, 0.9), lamp(3, 2, -5, 0.5, c.a), floor(c, 0, "#131317", 0.5),
              {"type": "mesh", "shape": "cylinder", "detail": 28, "x": 0, "y": 0.55, "z": -0.9, "scale": 1, "sx": 0.55, "sy": 0.4, "sz": 0.55, "rx": 0.25, **solid(c.b, 0.5, 0.2), "emit": "0.9*env.k"},
              drum(-0.75, 1.0, -0.55, 0.36, 0.12, "#d8d2c4", "0.9*env.s"), drum(0.8, 1.1, -0.6, 0.3, 0.1, c.c, 0),
              {"type": "mesh", "shape": "cylinder", "detail": 28, "x": 1.25, "y": 1.75, "z": -0.35, "scale": 1, "sx": 0.42, "sy": 0.012, "sz": 0.42, "rz": "0.03*env.h*sin(time.t*3)", "rx": 0.02, **solid("#c9a84a", 0.25, 1.0),
               "emit": "0.6*env.h"},
              box(1.25, 0.9, -0.35, 0.015, 0.85, 0.015, **solid("#777", 0.4, 0.8)), box(0, 0.5, 0.25, 0.22, 0.03, 0.22, **solid("#2a2a2e", 0.6)),
              {"type": "figure", "rig": "human", "motion": "none", "x": 0, "y": 1.02, "z": 0.25, "scale": 1.0, "ry": 0.5, **skin("#cfc8ba", 0.03),
               "pose": {"thigh_l": [0.2, 0, -0.04], "thigh_r": [0.2, 0, 0.04], "shin_l": [-0.2, 0, 0], "shin_r": ["0 - 0.2 + 0.05*env.k", 0, 0],
                        "arm_l": ["0.17 - 0.07*env.s", 0, -0.05], "forearm_l": ["0.1 + 0.12*env.s", 0, 0], "arm_r": ["0.2 - 0.06*env.h", 0, 0.09], "forearm_r": ["0.06 + 0.12*env.h", 0, 0],
                        "spine": ["0.02 + 0.015*env.k", 0, 0], "head": ["0.02*env.s", 0, 0]},
               "extra": [{"name": "stick_l", "parent": "forearm_l", "length": 0.5, "dir": [0, -1, 0.2], "width": 0.014}, {"name": "stick_r", "parent": "forearm_r", "length": 0.5, "dir": [0, -1, 0.2], "width": 0.014}]}]
    look = {"background": c.bg, "env": env, "layers": layers, "filters": post3d(-2, 5, -6, shadow=0.6)}
    return shots(c, look, [cam("0.8*sin(time.bar/7)", 1.7, -5.2, look=(0, 1.1, 0), zoom=1.6), cam(-3.6, 2.6, -2.2, look=(0, 1.0, -0.2), zoom=1.6), cam(2.8, 0.6, -3.4, look=(0, 1.2, 0), zoom=1.5)], k)


@idiom(needs=2, fam="lattice")
def hive(c):
    """A comb of six-sided cells with three ways across it: a riff runs along each, lighting
    the cells of its sixteenth, and where they cross is lighter."""
    P = c.riffs[:3]
    W, H = 19, 11
    col, row = f"(inst.i - {W}*floor(inst.i/{W}))", f"floor(inst.i/{W})"
    odd = f"(fract({row}/2)*2)"
    x, y = f"(({col} + 0.5*{odd}) - {(W - 1) / 2 + 0.25})*0.196", f"({(H - 1) / 2} - {row})*0.17"
    q = f"({col} - floor({row}/2))"
    axes = (q, row, f"({q} + {row})")
    layers = [{"type": "shape", "sides": 6, "rotate": 0.0833, "repeat": W * H, "radius": 0.106, "width": 0, "fill": 1, "color": c.dim, "opacity": 0.42, "x": x, "y": y}]
    for i, p in enumerate(P):
        d = f"(fract({p.turn} - {axes[i]}/{p.cell})*{p.cell})"
        layers.append({"type": "shape", "sides": 6, "rotate": 0.0833, "repeat": W * H, "radius": 0.1 - 0.018 * i, "width": 0, "fill": 1, "color": c.col(i), "blend": "add", "opacity": f"exp(0 - 1.0*{d})", "x": x, "y": y})
    return {"background": c.bg, "layers": layers, "filters": [bloom(c, 0.3, 0.014, 0.7)]}


@idiom(needs=1, fam="trace", paper=True, max_cell=13)
def changes(c):
    """Bells rung in changes: as many as the riff has sixteenths, each changing places with
    its neighbour row by row, hunting up to the back and down again, until they come round."""
    A = c.riffs[0]
    N = max(4, min(A.cell, 13))
    R = 26
    dx, dy = min(0.75, 8.0 / N), 0.19
    t = f"floor(time.beat*4 - {A.anchor:g} + 0.01)"

    def place(b, j):          # where bell b stands j rows ago
        sb = f"({b} + ({2 * N - 1} - 2*{b})*fract({b}/2)*2)"
        u = f"(fract(({t} - {j} + {sb})/{2 * N} + 0.0001)*{2 * N})"
        return f"min(floor({u} + 0.01), {2 * N - 1} - floor({u} + 0.01))"
    b, j = f"(inst.i - {N}*floor(inst.i/{N}))", f"floor(inst.i/{N})"
    X = lambda jj: f"(({place(b, jj)}) - {(N - 1) / 2})*{dx:g}"
    Y = lambda jj: f"(2.3 - ({jj} + fract(time.beat*4 - {A.anchor:g} + 0.01))*{dy})"
    lead = f"step({b}, 0.5)"
    layers = [{"type": "beam", "count": N * R, "from": [X(j), Y(j), 0], "to": [X(f"({j} + 1)"), Y(f"({j} + 1)"), 0], "width": f"0.012 + 0.03*{lead}", "glow": f"0.5 + 0.8*{lead}", "fade": 0, "color": c.dim, "samples": 3},
              {"type": "beam", "count": R, "from": [X("inst.i").replace(b, "0"), Y("inst.i"), -0.02], "to": [X("(inst.i + 1)").replace(b, "0"), Y("(inst.i + 1)"), -0.02], "width": 0.045, "glow": 1.2, "fade": 0,
               "color": c.a, "samples": 3},
              ball(X("0"), 2.3, -0.05, f"0.07 + 0.05*{A.hit}", 8, count=N, **glow(c.ink, 1.6))]
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.3, 0.014, 0.7)]}


@idiom(needs=1, fam="swing", cost=2)
def sympathy(c):
    """Two clocks hung from one beam laid across two chairs. They begin out of step, and by
    the end each swings exactly against the other."""
    A = c.riffs[0]
    off = f"(0.5 + 0.37*(1 - smooth(0.1, 0.9, {c.prog})))"
    th = (f"(0.07*sin({A.turn}))", f"(0.07*sin({A.turn} + {off}))")
    shove = f"(0.05*(sin({A.turn}) + sin({A.turn} + {off})))"
    wood = solid("#6b4a2e", 0.7)
    layers = [lamp(-3, 5, -6, 1.55), lamp(3, 2, -5, 0.85, c.a), floor(c, 0, "#1c1c24", 0.7), box(shove, 2.62, 0, 2.9, 0.05, 0.08, **wood)]
    for sx in (-1, 1):                                       # the chairs
        layers.append(box(sx * 2.6, 1.3, 0.25, 0.05, 1.3, 0.05, **wood))
        layers.append(box(sx * 2.6, 0.55, -0.15, 0.05, 0.55, 0.05, **wood))
        layers.append(box(sx * 2.6, 1.1, 0.05, 0.3, 0.04, 0.3, **wood))
        layers.append(box(sx * 2.6, 2.2, 0.25, 0.3, 0.25, 0.03, **wood))
    for i, (x, a) in enumerate(zip((-0.8, 0.8), th)):
        X = f"({shove} + {x})"
        layers.append(box(X, 2.15, 0, 0.3, 0.42, 0.12, **solid("#4a362c", 0.55)))
        layers.append({"type": "mesh", "shape": "cylinder", "detail": 24, "x": X, "y": 2.2, "z": -0.13, "scale": 1, "sx": 0.22, "sy": 0.01, "sz": 0.22, "rx": 0.25, **solid("#f2ece0", 0.4), "emit": 0.25})
        layers.append(box(f"{X} + 0.6*sin({a})", f"1.75 - 0.6*cos({a})", -0.05, 0.016, 0.6, 0.016, rz=a, **solid("#d8c07c", 0.28, 0.9)))
        layers.append({"type": "mesh", "shape": "cylinder", "detail": 20, "x": f"{X} + 1.2*sin({a})", "y": f"1.75 - 1.2*cos({a})", "z": -0.06, "scale": 1, "sx": 0.19, "sy": 0.028, "sz": 0.19, "rx": 0.25,
                       **solid("#e0c880", 0.28, 0.9), "emit": f"0.22 + 0.85*exp(0 - 5*abs(sin({A.turn}{' + ' + off if i else ''})))"})
    return {"background": c.bg, "camera": cam("0.8*sin(time.bar/10)", 1.6, -7, look=(0, 1.5, 0), zoom=1.8), "layers": layers, "filters": post3d(-3, 5, -6, shadow=0.6)}


@idiom(needs=1, fam="grow")
def colony(c):
    """A dish: a new cell for every note, until there are as many as it can hold; after
    that one goes for each that comes."""
    A = c.riffs[0]
    cap = 144
    born = f"(28 + (time.beat*4 - {c.a16:g})*{max(0.5, min(3.0, cap / max((c.b16 - c.a16) * 0.6, 8))):g})"
    k = f"(inst.i - {cap}*floor(({born} - inst.i)/{cap}))"         # which life this place is on
    age = f"(({born}) - inst.i - {cap}*floor(max({born} - inst.i, 0)/{cap}))"
    r = "(0.268*sqrt(inst.i + 0.5))"
    ang = "(inst.i*0.381966)"
    d = f"(fract({A.turn} - fract(inst.i/{A.cell}))*{A.cell})"
    size = f"0.13*step(0, {age})*smooth(0, 3, {age})*(1 - 0.5*smooth({cap - 12}, {cap}, {age}))*(1 + 0.3*exp(0 - 1.5*{d}))"
    layers = [{"type": "shape", "sides": 0, "radius": 1.36, "width": 0.006, "fill": 0, "color": c.dim},
              ball(f"{r}*cos({ang})", f"{r}*sin({ang})", 0, size, 8, count=cap, **glow(c.a, f"0.45 + 0.9*exp(0 - 1.2*{d})")),
              ball(f"{r}*cos({ang})", f"{r}*sin({ang})", -0.1, f"0.045*step(0, {age})", 6, count=cap, **glow(c.ink, 1.2))]
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.35, 0.016, 0.65)]}


@idiom(needs=0, tune=True, fam="paper", paper=True)
def score(c):
    """Written down as it is played: five lines, a head for each note at its height, a bar
    line every bar, and a red stroke each time the riff comes round."""
    T = (c.tunes + c.riffs + c.parts)[0]
    A = (c.riffs or [T])[0]
    ink, paper = "#17171a", "#ece6d6"
    v = 0.9
    x = f"(3.2 - {v}*note.age)"
    step_ = f"floor({T.pitch(0, 12.99)})"                   # the head's place on the lines and spaces (0: under the staff … 12: over it)
    y = f"(({step_} - 6)*0.11)"
    layers = [box(0, "(inst.i - 2)*0.22", 0.1, 4.7, 0.011, 0.01, count=5, **glow(ink, 1)),
              box(f"3.2 - {v}*(fract(time.bar) + inst.i)*4", 0, 0.08, 0.008, 0.44, 0.01, count=4, **glow(ink, 1)),
              box(f"3.2 - {v}*(fract({A.turn}) + inst.i)*{(A.cell or 16) / 4}", 0, 0.06, 0.012, 0.62, 0.01, count=8, **glow("#c8341d", 1)),
              {"type": "mesh", "shape": "sphere", "detail": 10, "notes": {"track": T.name, "past": 9}, "x": x, "y": y, "z": 0, "scale": 0.1, "sx": 1.25, "sy": 0.85, "sz": 0.3, "rz": 0.06, **glow(ink, 1)},
              box(f"{x} + 0.115", f"{y} + 0.3", 0, 0.008, 0.3, 0.01, notes={"track": T.name, "past": 9}, **glow(ink, 1)),
              box(3.2, 0, -0.05, 0.01, 0.9, 0.01, **glow("#c8341d", f"0.4 + 0.6*{A.hit}"), opacity=0.6)]
    return {"background": paper, "camera": FLAT, "layers": layers, "filters": [{"type": "grain", "amount": 0.04}]}


# ───────────────────────── an eighth lot: letters, games, growing things ─────────────────────────

def _letters(c):
    t = "".join(ch for ch in c.title.upper() if ch.isalpha())
    return t or "COMMONTIME"


@idiom(needs=1, fam="type", paper=True, max_cell=24)
def teletype(c):
    """A page typed by the riff: a key struck for every note, the song's name letter by
    letter with the sixteenths, and a new line each time the riff comes round. The name
    never falls in the same columns twice."""
    A = c.riffs[0]
    nn = A.cell
    w = min(0.62, 8.6 / nn)
    rows = 6
    turn_now = f"floor({A.turn})"
    row = f"({turn_now} - floor((note.beat*4 - {A.anchor:g} + 0.01)/{nn}))"       # lines ago
    layers = [{"type": "text", "notes": {"track": A.name, "past": rows * nn / 4}, "text": _letters(c), "pick": "floor(note.beat*4 + 0.01)", "size": min(0.26, w / 2.557 * 1.25), "align": "center", "width": 0.18, "skew": 0,
               "x": f"(({A.nstep} + 0.5 - {nn / 2})*{w / 2.557:g})", "y": f"0 - 0.74 + 0.3*{row} + 0.3*smooth(0, 0.15, fract({A.turn})) - 0.3", "color": c.ink, "opacity": "0.55 + 0.45*exp(0 - 2*note.age)"},
              box(f"((fract({A.turn})*{nn} + 0.5 - {nn / 2})*{w:g})", -2.3, 0, w * 0.4, 0.02, 0.01, **glow(c.a, 1.5))]
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.25, 0.012, 0.75)]}


@idiom(needs=0, fam="type")
def letters(c):
    """A rain of letters: every note lets one fall down the column of its sixteenth in the
    bar."""
    P = _cast(c, 3)
    layers = []
    for i, p in enumerate(P):
        top = 0.95 - i * 1.9 / len(P)                      # each part falls through its own band of the frame
        fall = 1.9 / len(P) - 0.26
        for e, (lag, op) in enumerate(((0, 1.0), (0.3, 0.4))):
            layers.append({"type": "text", "notes": {"track": p.name, "past": 6.1}, "text": _letters(c), "pick": f"floor(note.midi + {e} + 0.5)", "size": 0.24, "align": "center", "width": 0.17, "skew": 0,
                           "x": f"(({NOTE16} + 0.5 - 8)*0.21)", "y": f"{top:g} - {fall:g}*min((note.age - {lag})/1.2, 1) - 0.24", "color": c.ink if e else c.col(i),
                           "opacity": f"{op}*step({lag}, note.age)*(1 - 0.6*step(1.5, note.age))*(1 - smooth(3.5, 6, note.age))"})
    return {"background": c.bg, "layers": layers, "filters": [bloom(c, 0.4, 0.016, 0.6)]}


@idiom(needs=1, fam="count")
def odometer(c):
    """A counter for each riff: how many times it has come round, and where in itself it is."""
    P = c.riffs[:3]
    layers = []
    for i, p in enumerate(P):
        y = ((len(P) - 1) / 2 - i) * 0.56 - 0.17
        T = f"max({p.turn} - {(c.a16 - p.anchor) / p.cell:g}, 0)"            # turns since the scene began
        roll = f"smooth(0.85, 1, fract({T}))"
        for k, div in enumerate((100, 10, 1)):
            x = -0.75 + 0.34 * k
            # A wheel rolls only when the wheels to its right are on nine.
            carry = "1" if div == 1 else f"step(0.9, fract(floor({T})/{div}))"
            for nxt in (0, 1):
                layers.append({"type": "text", "text": "0123456789", "pick": f"floor(fract((floor({T}/{div}) + {nxt})/10 + 0.001)*10)", "size": 0.34, "align": "center", "width": 0.11, "skew": 0, "x": x,
                               "y": f"{y:g} + {0.34 if nxt == 0 else -0.34}*{roll}*{carry}*{1 if nxt == 0 else -1} + {0 if nxt == 0 else -0.34}*{carry} + {0 if nxt == 0 else 0.34}*{carry}*{roll}*0 "
                               if False else f"{y:g} + 0.3*{roll}*{carry}*{1 if nxt == 0 else 0} - 0.3*(1 - {roll})*{nxt}",
                               "color": c.ink, "opacity": f"1 - {roll}*{carry}" if nxt == 0 else f"{roll}*{carry}"})
        layers.append({"type": "text", "text": "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:max(1, min(p.cell, 26))], "pick": f"floor(fract({p.turn})*{p.cell} + 0.02)", "size": 0.34, "align": "center", "width": 0.11, "skew": 0,
                       "x": 0.55, "y": y, "color": c.col(i)})
        layers.append({"type": "shape", "sides": 4, "rotate": 0.125, "radius": 0.02, "width": 0, "fill": 1, "color": c.col(i), "x": 0.28, "y": y + 0.17, "glow": f"1 + 3*{p.hit}"})
    return {"background": c.bg, "layers": layers, "filters": [bloom(c, 0.3, 0.014, 0.7)]}


@idiom(needs=1, fam="field", cost=2)
def interference(c):
    """A field of dots swelling as two sets of rings pass through it, one from each riff,
    as far between rings as the riff is long."""
    A = c.riffs[0]
    B = c.riffs[1] if len(c.riffs) > 1 else A
    W, H = 48, 27
    col, row = f"(inst.i - {W}*floor(inst.i/{W}))", f"floor(inst.i/{W})"
    x, y = f"(({col} - {(W - 1) / 2})*0.074)", f"(({(H - 1) / 2} - {row})*0.074)"
    ka, kb = 3.2 * 5 / A.cell, 3.2 * 5 / B.cell
    d1, d2 = f"len({x} + 0.9, {y} - 0.2)", f"len({x} - 0.9, {y} + 0.25)"
    wave = f"(0.5 + 0.25*sin({d1}*{ka:g} - {A.turn}) + 0.25*sin({d2}*{kb:g} - {B.turn}))"
    layers = [{"type": "shape", "repeat": W * H, "sides": 1, "radius": f"0.004 + 0.036*{wave}", "width": 0, "fill": 1, "x": x, "y": y, "palette": [c.b, c.a, c.ink], "pos": wave},
              {"type": "shape", "sides": 1, "radius": f"0.02 + 0.03*{A.hit}", "width": 0, "fill": 1, "color": c.ink, "x": -0.9, "y": 0.2},
              {"type": "shape", "sides": 1, "radius": f"0.02 + 0.03*{B.hit}", "width": 0, "fill": 1, "color": c.ink, "x": 0.9, "y": -0.25}]
    return {"background": c.bg, "layers": layers, "filters": [bloom(c, 0.25, 0.012, 0.75)]}


@idiom(needs=1, fam="grow", cost=2)
def fractal(c):
    """A tree that forks and forks again; its even forks open and close with one riff and
    its odd forks with another, so it is never the same tree twice."""
    A = c.riffs[0]
    B = c.riffs[1] if len(c.riffs) > 1 else A
    bones, pose = [{"name": "t", "parent": None, "length": 0.9, "dir": [0, 1, 0], "width": 0.07}], {}

    def grow(name, level):
        if level > 5:
            return
        for side, sgn in (("l", -1), ("r", 1)):
            nm = name + side
            bones.append({"name": nm, "parent": name, "length": 0.82 * 0.74 ** level, "dir": [0, 1, 0], "width": 0.06 * 0.72 ** level})
            p = (A, B)[level % 2]
            pose[nm] = [f"0.012*sin({p.turn}/2 + {level * 0.13:.2f})", 0, f"{sgn}*(0.065 + 0.045*sin({p.turn} + {level * 0.07:.2f}))"]
            grow(nm, level + 1)
    grow("t", 1)
    layers = [lamp(-2, 5, -6, 0.9), lamp(3, 1, -5, 0.5, c.a),
              {"type": "figure", "bones": bones, "motion": "none", "pose": pose, "x": 0, "y": -2.2, "z": 0, "scale": 1.5, **skin(c.ink, f"0.25 + 0.5*{A.hit}"), "color": c.ink, "rim": 0.6, "rim_color": c.a, "melt": 0.03}]
    return {"background": c.bg, "camera": cam("0.5*sin(time.bar/9)", 0.2, -7, zoom=1.5), "layers": layers, "filters": [{"type": "tonemap", "knee": 0.8}, {"type": "aa"}, bloom(c, 0.4, 0.02, 0.6)]}


@idiom(needs=1, fam="grow", paper=True)
def treerings(c):
    """A trunk sawn through: a ring laid down each time the riff comes round, a knot in it
    for every note."""
    A = c.riffs[0]
    turns = max(3, (c.b16 - c.a16) / A.cell)
    seed_t = 2.0
    dr = min(0.15, 0.86 / (turns + seed_t + 1))
    T = f"({seed_t:g} + (time.beat*4 - {c.a16:g})/{A.cell})"
    layers = [{"type": "shape", "repeat": int(turns + seed_t) + 2, "sides": 0, "radius": f"{dr:g}*(inst.i + 1)*(1 + 0.014*noise(inst.i*3.1))", "width": f"{dr * 0.28:g}", "fill": 0, "color": c.dim,
               "opacity": f"step(inst.i, {T})*(0.45 + 0.55*step({T} - 1, inst.i))"},
              {"type": "shape", "sides": 0, "radius": f"{dr:g}*({T} + 1)", "width": f"{dr * 0.36:g}", "fill": 0, "color": c.a},
              {"type": "shape", "notes": {"track": A.name, "past": (turns + seed_t) * A.cell / 4 + 1}, "sides": 1, "radius": f"{dr * 0.25:g}*(0.65 + note.vel)*(1 + 1.1*exp(0 - 2*note.age))", "width": 0, "fill": 1, "color": c.ink,
               "x": f"{dr:g}*({seed_t:g} + (note.beat*4 - {c.a16:g})/{A.cell} + 1)*sin({A.nph})", "y": f"{dr:g}*({seed_t:g} + (note.beat*4 - {c.a16:g})/{A.cell} + 1)*cos({A.nph})", "opacity": f"step({c.a16 / 4 - seed_t * A.cell / 4:g}, note.beat)"}]
    return {"background": c.bg, "layers": layers, "filters": [bloom(c, 0.3, 0.014, 0.7)]}


@idiom(needs=1, fam="body", cost=2, max_cell=24)
def eye(c):
    """An eye. Its iris has a spoke for each sixteenth of the riff and turns with it; the
    pupil opens to the low end; it blinks as the riff comes round."""
    A = c.riffs[0]
    nn = A.cell
    d = f"(fract({A.turn} - inst.i/{nn})*{nn})"
    lid = f"(1 - 0.92*exp(0 - 9*fract({A.turn}/2)))"                 # open, but for a blink every second turn
    th = f"(inst.i/{nn} + {A.turn}/{nn})"
    layers = [{"type": "shape", "sides": 1, "radius": 0.74, "width": 0, "fill": 1, "color": "#e9e6df", "blend": "normal"},
              {"type": "shape", "sides": 1, "radius": 0.5, "width": 0, "fill": 1, "color": c.b, "blend": "normal"},
              box(f"0.83*sin({th})", f"0.83*cos({th})", 0, 0.05, 0.42, 0.01, count=nn, rz=f"0 - {th}", **glow(c.a, f"0.5 + 1.6*exp(0 - 1.4*{d})")),
              {"type": "shape", "sides": 1, "radius": "0.17 + 0.16*audio.low", "width": 0, "fill": 1, "color": "#000000", "blend": "normal"},
              {"type": "shape", "sides": 1, "radius": 0.05, "width": 0, "fill": 1, "color": "#ffffff", "x": -0.1, "y": 0.1},
              {"type": "shape", "sides": 4, "rotate": 0.125, "radius": 2.6, "width": 0, "fill": 1, "color": c.bg, "blend": "normal", "x": 0, "y": f"1.84 + 0.72*{lid}"},
              {"type": "shape", "sides": 4, "rotate": 0.125, "radius": 2.6, "width": 0, "fill": 1, "color": c.bg, "blend": "normal", "x": 0, "y": f"0 - 1.84 - 0.72*{lid}"}]
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [{"type": "lens", "x": 0, "y": 0, "ring": 0} if False else {"type": "grain", "amount": 0.03}, bloom(c, 0.3, 0.02, 0.8)]}


@idiom(needs=2, fam="game")
def pong(c):
    """An old game: the ball goes from bat to bat once for each turn of one riff, and from
    wall to wall once for each turn of the other. The score is how often each has come round."""
    A, B = c.riffs[0], c.riffs[1]
    bx, by = f"(1.45*tri({A.turn}/2))", f"(0.78*tri({B.turn}/2 + 0.12))"
    net = {"type": "shape", "repeat": 15, "sides": 4, "rotate": 0.125, "radius": 0.022, "width": 0, "fill": 1, "color": c.dim, "x": 0, "y": "(inst.i - 7)*0.125"}
    bat = lambda x, lag: {"type": "shape", "sides": 4, "rotate": 0.125, "radius": 0.03, "width": 0, "fill": 1, "color": c.ink, "x": x, "y": f"(0.78*tri({B.turn}/2 + 0.12 - {lag}))", "scale": 1, "count": 1}
    layers = [net]
    for x, lag in ((-1.55, 0.004), (1.55, 0.008)):
        layers.append({"type": "shape", "repeat": 5, "sides": 4, "rotate": 0.125, "radius": 0.028, "width": 0, "fill": 1, "color": c.ink, "x": x, "y": f"(0.78*tri({B.turn}/2 + 0.12 - {lag})) + (inst.i - 2)*0.038"})
    layers.append({"type": "shape", "sides": 4, "rotate": 0.125, "radius": 0.036, "width": 0, "fill": 1, "color": c.a, "x": bx, "y": by, "glow": f"0.7 + 1.5*{A.hit}"})
    # Luminous trailing ghosts behind the ball so its diagonal path reads across beats.
    for k_t, lag in enumerate((0.015, 0.03, 0.048), 1):
        layers.append({"type": "shape", "sides": 4, "rotate": 0.125, "radius": 0.032 - 0.005 * k_t, "width": 0, "fill": 1, "color": c.a,
                       "x": f"(1.45*tri({A.turn}/2 - {lag}))", "y": f"(0.78*tri({B.turn}/2 + 0.12 - {lag}))", "opacity": 0.55 - 0.14 * k_t})
    for p, x, col in ((A, -0.45, c.a), (B, 0.45, c.b)):
        T = f"floor({p.turn} - {(c.a16 - p.anchor) / p.cell:g} + 0.001)"
        for k, div in enumerate((10, 1)):
            layers.append({"type": "text", "text": "0123456789", "pick": f"floor(fract(floor({T}/{div})/10 + 0.001)*10)", "size": 0.2, "align": "center", "width": 0.12, "skew": 0, "x": x + (k - 0.5) * 0.17, "y": 0.62, "color": col})
    for y in (-0.9, 0.9):
        layers.append({"type": "shape", "sides": 4, "rotate": 0.125, "radius": 2.3, "width": 0, "fill": 1, "color": c.dim, "blend": "normal", "x": 0, "y": y + (1.64 if y > 0 else -1.64), "opacity": 0.35})
    return {"background": c.bg, "layers": layers, "filters": [bloom(c, 0.3, 0.014, 0.7)]}


@idiom(needs=0, fam="game")
def invaders(c):
    """Another old game: the ranks march a step a sixteenth, common time's own tread, and
    every note is a shot sent up at them."""
    P = _cast(c, 2)
    W, H = 11, 4
    col, row = f"(inst.i - {W}*floor(inst.i/{W}))", f"floor(inst.i/{W})"
    march = "(0.35*(tri(time.bar/2)*2 - 1) - fract(0) )" if False else "(0.36*(floor(tri(time.bar/2 + 0.25)*16)/8 - 1))"
    foot = "step(0.5, fract(time.beat*2))"
    X, Y = f"(({col} - {(W - 1) / 2})*0.21 + {march})", f"(0.72 - {row}*0.17 - 0.04*floor(fract(time.bar/8)*8))"
    layers = [{"type": "shape", "repeat": W * H, "sides": 4, "rotate": 0.125, "radius": 0.068, "width": 0, "fill": 1, "x": X, "y": Y, "palette": [c.a, c.b, c.c], "pos": f"{row}/4"},
              {"type": "shape", "repeat": W * H, "sides": 4, "rotate": 0.125, "radius": 0.026, "width": 0, "fill": 1, "color": c.bg, "blend": "normal", "x": f"{X} - 0.02 + 0.04*{foot}", "y": f"{Y} + 0.012"},
              {"type": "shape", "repeat": W * H, "sides": 4, "rotate": 0.125, "radius": 0.022, "width": 0, "fill": 1, "x": f"{X} + (0.045 - 0.09*fract(inst.i/2)*2)*(0.5 + {foot})", "y": f"{Y} - 0.05",
               "palette": [c.a, c.b, c.c], "pos": f"{row}/4"}]
    for i, p in enumerate(P):
        nn = p.cell or 16
        layers.append({"type": "shape", "notes": {"track": p.name, "past": 3}, "sides": 4, "rotate": 0.125, "radius": 0.022, "width": 0, "fill": 1, "color": c.ink, "x": f"(({p.nstep} + 0.5)/{nn} - 0.5)*2.6",
                       "y": f"0 - 0.86 + 0.75*note.age", "opacity": "step(note.age, 2.3)", "glow": 1.1})
        layers.append({"type": "shape", "sides": 4, "rotate": 0.125, "radius": 0.06, "width": 0, "fill": 1, "color": c.col(i), "x": f"((floor(fract({p.turn})*{nn}) + 0.5)/{nn} - 0.5)*2.6", "y": -0.9 - 0.04 * i, "glow": 0.6})
    return {"background": c.bg, "layers": layers, "filters": [bloom(c, 0.3, 0.014, 0.7)]}


# ───────────────────────── a ninth lot: places and grounds ─────────────────────────

@idiom(needs=1, fam="place", cost=2, max_cell=16)
def skyline(c):
    """A town at night: a tower for each riff, as many windows across as the riff has
    sixteenths and a floor for each time it comes round. Every note puts a light on."""
    P = c.riffs[:3]
    floors = 9
    layers = [{"type": "sky", "zenith": "#080b1a", "horizon": "#26315e", "ground": "#080a10", "sun": "#f4f1e6", "sun_yaw": 0.06, "sun_height": 0.2, "sun_size": 0.05, "clouds": 0},
              {"type": "stars", "count": 300, "size": 0.002, "twinkle": 0.4, "opacity": 0.75}, floor(c, 0, "#0b0d14", 0.45)]
    wide = sum(p.cell for p in P) * 0.3 + (len(P) - 1) * 1.0
    x0 = -wide / 2
    for i, p in enumerate(P):
        w = p.cell * 0.3
        cx = x0 + w / 2
        h = floors * 0.44 + 0.3
        layers.append(box(cx, h / 2, 0.6, w / 2 + 0.1, h / 2, 0.5, **solid("#11131c", 0.6)))
        col, row = f"(inst.i - {p.cell}*floor(inst.i/{p.cell}))", f"floor(inst.i/{p.cell})"
        layers.append(box(f"{cx - w / 2 + 0.15:g} + {col}*0.3", f"0.4 + {row}*0.44", 0.08, 0.09, 0.13, 0.01, count=p.cell * floors, **glow("#1c2030", 1)))
        turn_of = f"floor((note.beat*4 - {p.anchor:g} + 0.01)/{p.cell})"
        row_n = f"(fract(({turn_of})/{floors} + 0.0001)*{floors})"
        fresh = f"step(floor({p.turn}) - {turn_of}, {floors} - 0.5)"
        layers.append(box(f"{cx - w / 2 + 0.15:g} + {p.nstep}*0.3", f"0.4 + floor({row_n} + 0.01)*0.44", 0.05, 0.09, 0.13, 0.01, notes={"track": p.name, "past": floors * p.cell / 4},
                          **glow(c.col(i), f"{fresh}*(0.9 + 2.5*exp(0 - 3*note.age))"), opacity=fresh))
        x0 += w + 1.0
    look = {"background": "#05060f", "layers": layers, "filters": [{"type": "reflect", "y": 0, "amount": 0.35} if False else {"type": "tonemap", "knee": 0.8}, {"type": "aa"}, bloom(c, 0.5, 0.02, 0.55)]}
    return shots(c, look, [cam("1.2*sin(time.bar/9)", 2.2, -9.5, look=(0, 2.2, 0), zoom=1.5), cam(-wide / 2 - 2, 0.5, -4, look=(0, 2.4, 0.5), zoom=1.3), cam(0.5, 4.2, -5, look=(0, 2.0, 0.5), zoom=1.2)], P[0])


@idiom(needs=1, fam="flock", cost=2)
def murmur(c):
    """Starlings at dusk: the flock goes where two riffs send it, each bird a little behind
    the one before, so its shape is the path it has just taken."""
    A = c.riffs[0]
    B = c.riffs[1] if len(c.riffs) > 1 else A
    n_ = 420
    lag = "(hash(inst.i*1.37)*2.4)"                          # beats behind the head of the flock
    tA = f"(((time.beat - {lag})*4 - {A.anchor:g})/{A.cell})"
    tB = f"(((time.beat - {lag})*4 - {B.anchor:g})/{B.cell * (2 if B is A else 1)})"
    x = f"3.6*sin({tA}/2) + 0.5*noise3(inst.i*0.71, time.beat*0.2, 0)"
    y = f"2.4 + 1.3*sin({tB}/2 + 0.1) + 0.4*noise3(inst.i*0.53, 7, time.beat*0.2)"
    z = f"3 + 2.0*cos({tA}/2) + 0.6*noise3(3, inst.i*0.61, time.beat*0.2)"
    layers = [{"type": "sky", "zenith": "#2c3f68", "horizon": c.a, "ground": "#0d0e14", "sun": "#ffe2b0", "sun_yaw": 0.02, "sun_height": 0.02, "sun_size": 0.05, "clouds": 0.25, "cloud_height": 5},
              ball(x, y, z, f"0.035 + 0.02*hash(inst.i*3.1) + 0.02*{A.hit}", 4, count=n_, **glow("#07080c", 1), sx=1.8, sy=0.6),
              box("(inst.i - 6)*1.6", 0.5, 9, 0.02, 0.5, 0.02, count=13, **glow("#07080c", 1)),
              box(0, 0.9, 9, 12, 0.008, 0.008, **glow("#07080c", 1))]
    return {"background": "#2c3f68", "camera": cam(0, 0.5, -6, look=(0, 2.2, 3), zoom=1.2), "layers": layers, "filters": [{"type": "tonemap", "knee": 0.85}, {"type": "aa"}]}


@idiom(needs=1, fam="type")
def splitflap(c):
    """A departures board: a row for each riff, its letters turning over every sixteenth and
    falling into the song's name for the moment the riff comes round. All the rows read
    true together only where the riffs meet."""
    P = c.riffs[:4]
    name = _letters(c)[:14]
    n_ = len(name)
    w = min(0.2, 3.0 / n_)
    layers = []
    for i, p in enumerate(P):
        y = ((len(P) - 1) / 2 - i) * 0.4
        home = f"step(fract({p.turn})*{p.cell}, 1.0)"       # the riff's first sixteenth
        scr = f"floor(hash(floor(time.beat*4 + 0.01)*1.7 + inst.i*7.3 + {i * 13})*26)"
        layers.append({"type": "shape", "repeat": n_, "sides": 4, "rotate": 0.125, "radius": w * 0.62, "width": 0, "fill": 1, "color": "#26282f", "blend": "normal", "x": f"(inst.i - {(n_ - 1) / 2})*{w:g}", "y": y})
        layers.append({"type": "text", "repeat": n_, "text": name + "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "pick": f"mix({n_} + {scr}, inst.i, {home})", "size": w * 1.05, "align": "center", "width": 0.14, "skew": 0,
                       "x": f"(inst.i - {(n_ - 1) / 2})*{w:g}", "y": y - w * 0.52, "color": c.ink, "opacity": f"0.85 + 0.15*{home}"})
        layers.append({"type": "shape", "repeat": n_, "sides": 4, "rotate": 0.125, "radius": w * 0.62, "width": 0, "fill": 1, "color": c.col(i), "blend": "add", "opacity": f"0.45*{home}",
                       "x": f"(inst.i - {(n_ - 1) / 2})*{w:g}", "y": y})
        layers.append(box(0, y * 2.557, -0.1, n_ * w * 2.557 / 2 + 0.1, 0.008, 0.01, **glow(c.bg, 1)))
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.25, 0.012, 0.8)]}


@idiom(needs=2, fam="game", max_cell=24)
def fruit(c):
    """Three reels, each with as many pictures as its riff has sixteenths, each going a
    picture a sixteenth. They show three of a kind on the line only where the riffs meet."""
    P = c.riffs[:3]
    layers = []
    for i, p in enumerate(P):
        x = (i - (len(P) - 1) / 2) * 0.98
        nn = p.cell
        off = f"(fract((inst.i - floor(fract({p.turn})*{nn} + 0.01) - smooth(0.6, 1, fract(fract({p.turn})*{nn})))/{nn} + 0.5) - 0.5)*{nn}"
        kind = f"(inst.i - 5*floor(inst.i/5))"
        layers.append({"type": "shape", "sides": 4, "rotate": 0.125, "radius": 0.64, "width": 0, "fill": 1, "color": "#eeeae0", "blend": "normal", "x": x, "y": 0})
        layers.append({"type": "shape", "repeat": nn, "sides": f"3 + {kind}", "radius": f"0.2*step(abs({off}), 1.4)", "width": 0, "fill": 1, "x": x, "y": f"({off})*0.49", "blend": "normal",
                       "palette": [c.a, c.b, c.c, "#222226", c.a], "pos": f"{kind}/5", "star": f"0.5*step({kind}, 0.5)", "rotate": 0.25})
        layers.append({"type": "shape", "sides": 4, "rotate": 0.125, "radius": 0.68, "width": 0.012, "fill": 0, "color": c.dim, "x": x, "y": 0})
    for y in (-1, 1):
        layers.append({"type": "shape", "sides": 4, "rotate": 0.125, "radius": 2.4, "width": 0, "fill": 1, "color": c.bg, "blend": "normal", "x": 0, "y": y * (0.46 + 1.7)})
    meet = " * ".join(f"step(fract({p.turn})*{p.cell}, 1.0)" for p in P)
    layers.append({"type": "shape", "sides": 4, "rotate": 0.125, "radius": 1.2, "width": 0.01, "fill": 0, "color": c.ink, "x": 0, "y": 0, "opacity": 0})
    layers.append(box(0, 0, -0.2, 4.3, 0.012, 0.01, **glow(c.ink, f"0.6 + 4*{meet}")))
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, f"0.25 + 1.5*{meet}", 0.02, 0.75)]}


@idiom(needs=1, fam="game", max_cell=16)
def tetris(c):
    """A well as wide as the riff is long: every note drops a block into the column of its
    sixteenth, and each time the riff comes round a new row begins on top of the last."""
    P = [p for p in c.riffs if p.cell >= 5][:2]
    if not P:
        raise ValueError("no riff long enough to be a well")
    rows = 11
    layers = []
    for i, p in enumerate(P):
        nn = p.cell
        s_ = min(0.4, 3.6 / max(nn, sum(q.cell for q in P) / 1.0) * (1 if len(P) == 1 else 0.9))
        x0 = (i - (len(P) - 1) / 2) * (4.3 if len(P) > 1 else 0) - nn * s_ / 2
        turn_of = f"floor((note.beat*4 - {p.anchor:g} + 0.01)/{nn})"
        now = f"floor({p.turn})"
        rest = f"({turn_of} - max({now} - {rows - 1}, 0))"                      # the row it comes to rest in (the well scrolls once it is full)
        y = f"max(-2.1 + {s_:g}*{rest}, 2.3 - 9*note.age)"
        layers.append(box(x0 + nn * s_ / 2, -2.1 - s_ / 2 - 0.03, 0, nn * s_ / 2 + 0.04, 0.02, 0.02, **glow(c.dim, 1)))
        for sx in (-0.04, nn * s_ + 0.04):
            layers.append(box(x0 + sx, 0.1, 0, 0.02, 2.25, 0.02, **glow(c.dim, 1)))
        layers.append(box(f"{x0 + s_ / 2:g} + {p.nstep}*{s_:g}", y, 0, s_ * 0.44, s_ * 0.44, 0.05, notes={"track": p.name, "past": rows * nn / 4}, **glow(c.col(i), "0.75 + 2*exp(0 - 4*note.age)"),
                          opacity=f"step(0 - 0.5, {rest})"))
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.3, 0.014, 0.7)]}


@idiom(needs=1, fam="place", cost=3)
def wheat(c):
    """A field in the wind: a gust crosses it each time a riff comes round, one riff's from
    the left and the other's from behind."""
    A = c.riffs[0]
    B = c.riffs[1] if len(c.riffs) > 1 else A
    W_, D_ = 44, 22
    col, row = f"(inst.i - {W_}*floor(inst.i/{W_}))", f"floor(inst.i/{W_})"
    x, z = f"(({col} - {(W_ - 1) / 2})*0.3 + 0.1*hash(inst.i*1.3))", f"({row}*0.42 + 0.15*hash(inst.i*2.7))"
    gust = f"(0.11*exp(0 - 5*fract({A.turn} - ({x} + 7)/14)) + 0.03*sin(time.beat/5 + {x}/6))"
    gust2 = f"(0.09*exp(0 - 5*fract({B.turn} - {z}/9.5)))"
    layers = [{"type": "sky", "zenith": "#3f74c4", "horizon": "#e9eef0", "ground": "#8a7a3c", "sun": "#fff4dc", "sun_yaw": 0.3, "sun_height": 0.12, "clouds": 0.5}, floor(c, 0, "#7d6f38", 0.95),
              box(f"{x} + 0.55*sin({gust})", f"0.55*cos({gust})*cos({gust2})", f"{z} + 0.55*sin({gust2})", 0.012, 0.55, 0.012, count=W_ * D_, rz=f"0 - {gust}", rx=gust2, **solid("#ecc44e", 0.8), emit=0.15),
              ball(f"{x} + 1.12*sin({gust})", f"1.1*cos({gust})*cos({gust2})", f"{z} + 1.12*sin({gust2})", 0.06, 4, count=W_ * D_, sy=2.4, **solid("#f6dc7c", 0.8), emit=0.2)]
    return {"background": "#e9eef0", "camera": cam("0.8*sin(time.bar/11)", 1.6, -3.2, look=(0, 0.9, 4), zoom=1.25), "layers": layers,
            "filters": [{"type": "atmos", "amount": 0.6, "density": 0.03, "falloff": 0.4, "shafts": 0.2}, {"type": "tonemap", "knee": 0.8}, {"type": "aa"}]}


@idiom(needs=1, fam="ground", cost=2)
def thermal(c):
    """Seen by its heat: bands of colour, as many as the riff has sixteenths, that jump on
    a step each time it sounds."""
    A = c.riffs[0]
    B = c.riffs[1] if len(c.riffs) > 1 else A
    return {"background": c.bg, "vars": {"go": {"integrate": f"0.15 + 2.5*{A.hit}"}},
            "layers": [{"type": "plasma", "scale": f"1.2 + 0.25*sin({B.turn})", "speed": f"0.1 + 1.2*{A.hit}", "warp": 0.9, "spread": 1.0, "shade": 0, "light": 1, "pos": f"floor({A.turn}*{A.cell})/{A.cell}",
                        "palette": ["#0b0b2e", "#4a148c", c.b, c.a, "#ffd54a", "#fff7e0"]}],
            "filters": [{"type": "posterize", "levels": max(3, min(A.cell, 12))}, {"type": "outline", "amount": 0.35, "gain": 3, "width": 0.003, "color": "#000000"} if False else {"type": "grain", "amount": 0.05}]}


@idiom(needs=1, fam="ground", max_cell=24)
def testcard(c):
    """A test card: a row of colour bars for each riff, as many bars as it has sixteenths,
    moved along one each sixteenth; common time's sixteen greys run along the foot."""
    P = c.riffs[:3]
    rows = len(P)
    hgt = 1.56 / rows
    layers = []
    bars = ("#f0f0ec", "#e6d21e", "#19c8c8", "#1fc23a", "#c81fc0", "#d21f1f", "#1f2fd2", "#101014")
    for i, p in enumerate(P):
        nn = p.cell
        w = 3.56 / nn
        y = 0.94 - hgt * (i + 0.5)
        for q_, colour in enumerate(bars):
            n_q = len(range(q_, nn, 8))
            if not n_q:
                continue
            kk = f"({q_} + 8*inst.i)"                       # which bar this is
            place = f"(fract(({kk} + floor(fract({p.turn})*{nn} + 0.01))/{nn} + 0.0001)*{nn})"
            layers.append(box(f"((floor({place}) + 0.5)*{w:g} - 1.78)*2.557", y * 2.557, 0, w * 2.557 / 2 + 0.005, hgt * 2.557 / 2 + 0.005, 0.01, count=n_q, round=0, **glow(colour, 1)))
    layers.append(box("((inst.i + 0.5)*0.2225 - 1.78)*2.557", -0.81 * 2.557, 0, 0.2225 * 2.557 / 2 + 0.005, 0.19 * 2.557 / 2, 0.01, count=16, round=0,
                      **glow("#ffffff", "0.06 + 0.94*fract((inst.i + floor(fract(time.bar)*16 + 0.01))/16)")))
    layers.append({"type": "shape", "sides": 0, "radius": 0.52, "width": 0.012, "fill": 0, "color": "#f0f0ec"})
    layers.append({"type": "shape", "sides": 0, "radius": 0.06, "width": 0.008, "fill": 0, "color": "#f0f0ec"})
    return {"background": "#101014", "camera": FLAT, "layers": layers, "filters": [{"type": "scanlines", "amount": 0.12, "count": 270, "speed": 0}, {"type": "chroma", "amount": 0.003, "angle": 0},
                                                                                {"type": "vignette", "amount": 0.5}]}


@idiom(needs=1, fam="count", max_cell=36)
def leader(c):
    """The leader on a reel of film: the hand goes round once for each turn of the riff, and
    the figure in the ring counts the sixteenths it has left."""
    A = c.riffs[0]
    nn = A.cell
    left = f"({nn} - floor(fract({A.turn})*{nn} + 0.01))"
    grey = "#b9b4a6"
    layers = [{"type": "shape", "sides": 4, "rotate": 0.125, "radius": 2.6, "width": 0, "fill": 1, "color": "#6f6b60", "blend": "normal"},
              {"type": "shape", "sides": 4, "rotate": 0.125, "radius": 2.6, "width": 0, "fill": 1, "color": "#4d4a43", "blend": "normal", "x": 0, "y": 0, "opacity": f"step(0.5, fract(floor({A.turn})/2))"},
              box(0, 0, 0.2, 4.6, 0.006, 0.01, **glow("#1a1a1a", 1)), box(0, 0, 0.2, 0.006, 2.6, 0.01, **glow("#1a1a1a", 1)),
              {"type": "shape", "sides": 0, "radius": 0.8, "width": 0.012, "fill": 0, "color": "#1a1a1a", "blend": "normal"},
              {"type": "shape", "sides": 0, "radius": 0.68, "width": 0.008, "fill": 0, "color": "#1a1a1a", "blend": "normal"},
              box(f"1.1*sin(fract({A.turn}))", f"1.1*cos(fract({A.turn}))", 0.1, 0.012, 1.1, 0.01, rz=f"0 - fract({A.turn})", **glow("#1a1a1a", 1))]
    for k, div in enumerate((10, 1)):
        layers.append({"type": "text", "text": "0123456789", "pick": f"floor(fract(floor({left}/{div})/10 + 0.001)*10)", "size": 0.62, "align": "center", "width": 0.16, "skew": 0, "x": (k - 0.5) * 0.44 if nn >= 10 else 0,
                       "y": -0.31, "color": "#141414", "blend": "normal", "opacity": 1 if (nn >= 10 or k == 1) else 0})
    return {"background": grey, "camera": FLAT, "layers": layers, "filters": [{"type": "grain", "amount": 0.12}, {"type": "vignette", "amount": 0.6},
                                                                             {"type": "color", "brightness": f"0.04*noise(time.t*19)", "contrast": 1.05, "saturation": 0.2}]}


# ───────────────────────── a tenth lot: lights, cables, and people at play ─────────────────────────

def _zig(u):
    """Over and back: −1 at a whole number, 1 half way to the next."""
    return f"(1 - 2*abs(2*fract({u}) - 1))"


@idiom(needs=2, fam="game", max_cell=32)
def billiard(c):
    """One ball on a table: across it once for every turn of one riff, along it once for
    every turn of the other. It finds a corner only where the two riffs begin together."""
    A, B = c.riffs[0], c.riffs[1]
    Wt, Ht = 3.7, 1.95
    x, y = f"{Wt}*{_zig(f'{A.turn}/2')}", f"{Ht}*{_zig(f'{B.turn}/2')}"
    meet = f"exp(0 - 2.5*fract({A.turn})*{A.cell})*exp(0 - 2.5*fract({B.turn})*{B.cell})"
    felt = "#0f2a22" if c.variant % 2 == 0 else "#1a1830"
    layers = [box(0, 0, 0.3, Wt + 0.25, Ht + 0.25, 0.05, **glow("#2a1c12", 1)), box(0, 0, 0.2, Wt, Ht, 0.05, **glow(felt, 1)),
              # Rail sights (diamonds along top/bottom) and centre baulk line so the table reads immediately.
              box(0, 0, 0.15, 0.008, Ht, 0.01, **glow(c.dim, 0.35)),
              ball(f"(inst.i - 3)*{Wt * 0.31:g}", Ht + 0.12, 0.05, 0.045, 4, count=7, **glow(c.ink, 0.65)),
              ball(f"(inst.i - 3)*{Wt * 0.31:g}", -(Ht + 0.12), 0.05, 0.045, 4, count=7, **glow(c.ink, 0.65)),
              ball(f"(inst.i - 2*floor(inst.i/2) - 0.5)*{2 * Wt}", f"(floor(inst.i/2) - 0.5)*{2 * Ht}", 0, f"0.16 + 0.5*{meet}", 10, count=4, **glow(c.ink, f"0.35 + 6*{meet}")),
              {"type": "trail", "x": x, "y": y, "z": 0, "length": f"clamp(scene.t + 3.0, 3.0, {min(40.0, (c.b16 - c.a16) * c.six + 3.0):g})", "samples": 1600, "width": 0.016, "taper": 0, "glow": 0.85, "fade": 0.55, "color": c.b},
              ball(x, y, -0.05, f"0.13 + 0.06*{A.hit}", 12, **glow(c.a, f"1.8 + 2*{A.hit}"))]
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.35, 0.016, 0.6)]}


@idiom(needs=1, fam="thread", max_cell=24)
def star(c):
    """As many pins round a ring as the riff has sixteenths, and a thread laid a stroke a
    sixteenth: to the next pin in its first turn, to the next but one in its second, so each
    turn of the riff draws the next star that many points can make."""
    P = [p for p in c.riffs[:2] if 5 <= p.cell <= 24]
    if not P:
        raise ValueError("too few points for a star")
    layers = []
    for i, p in enumerate(P):
        n_, R = p.cell, (2.15, 1.05)[i]
        kmax = max(1, (n_ - 1) // 2)
        t0 = math.floor((c.a16 - p.anchor) / n_)
        turn = f"(floor({p.turn}) - {t0})"
        ph = f"(fract({p.turn})*{n_})"
        pin = lambda j: (f"{R}*sin(({j})/{n_})", f"{R}*cos(({j})/{n_})")  # noqa: E731
        for back, op in ((1, f"0.3*(1 - fract({p.turn}))"), (0, f"step(inst.i, {ph})*(0.4 + 0.6*exp(0 - 0.7*({ph} - inst.i)))")):
            kk = f"(1 + fract(({turn} - {back} + {kmax * 64})/{kmax} + 0.001)*{kmax} - 0.001*{kmax})"
            kk = f"floor({kk} + 0.01)"
            x1, y1 = pin("inst.i")
            x2, y2 = pin(f"inst.i + {kk}")
            layers.append({"type": "beam", "repeat": n_, "from": [x1, y1, 0], "to": [x2, y2, 0], "width": 0.03 if not back else 0.018, "glow": 1.35, "samples": 24, "color": c.col(i) if not back else c.dim, "opacity": op})
        x, y = pin("inst.i")
        layers.append(ball(x, y, -0.02, f"0.065 + 0.08*exp(0 - 1.5*fract({p.turn} - inst.i/{n_})*{n_})", 8, count=n_, **glow(c.ink, f"0.85 + 2.8*exp(0 - 1.5*fract({p.turn} - inst.i/{n_})*{n_})")))
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.4, 0.018, 0.55)]}


@idiom(needs=0, fam="fall")
def snow(c):
    """Snow: a flake for every note, as big as the note was loud, and the drift at the foot
    of the frame deepens through the scene."""
    P = _cast(c, 3)
    layers = [{"type": "gradient", "palette": ["#0b1226", "#141c38", "#27325a"], "angle": 0.25, "spread": 0.6, "res": 0.5},
              {"type": "motes", "mode": "drift", "count": 220, "w": 9, "h": 5, "d": 4, "y": 0, "z": 1, "fall": 0.55, "wind_x": 0.15, "wobble": 0.25, "size": 0.018, "glow": 0.45, "twinkle": 0.35, "color": "#dce4ff"}]
    for i, p in enumerate(P):
        sway = f"0.07*sin(note.age/5 + hash(note.i*3.1 + {i}))"
        layers.append({"type": "shape", "notes": {"track": p.name, "past": 11}, "sides": 6, "star": 0.55, "radius": f"0.03 + 0.045*note.vel + {0.012 * i}", "width": 0.005, "fill": 0.15,
                       "rotate": f"(hash(note.i*1.7) - 0.5)*note.age*0.08", "x": f"(hash(note.i*7.31 + {i * 5})*2 - 1)*1.72 + {sway}", "y": f"1.08 - (0.19 + 0.05*hash(note.i*2.3))*note.age",
                       "color": ("#f4f6ff", c.a, c.b)[i], "opacity": "1 - smooth(9, 11, note.age)"})
    layers.append({"type": "shape", "sides": 4, "rotate": 0.125, "radius": 2.6, "width": 0, "fill": 1, "color": "#e9edf7", "blend": "normal", "x": 0, "y": f"0 - 2.838 + 0.06 + 0.3*{c.prog}"})
    return {"background": "#0b1226", "layers": layers, "filters": [bloom(c, 0.35, 0.02, 0.6)]}


@idiom(needs=1, fam="engine")
def lifts(c):
    """Lifts: a shaft for each part, and its car goes to the floor of whatever note it plays;
    the counterweight goes the other way."""
    P = _cast(c, 5)
    floors = 7
    vars_ = {f"y{i}": {"follow": f"floor(track.{p.name}.key*{floors - 1} + 0.5)/{floors - 1}", "attack": "110ms", "release": "110ms"} for i, p in enumerate(P)}
    env = hit_env(P, "400ms")
    span, gapx = 3.9, min(1.7, 7.6 / len(P))
    layers = [box(0, 0, 0.4, len(P) * gapx / 2 + 0.3, span / 2 + 0.35, 0.05, **glow("#101116", 1)),
              box(0, f"(inst.i - {(floors - 1) / 2})*{span / (floors - 1):g} - 0.27", 0.3, len(P) * gapx / 2 + 0.3, 0.012, 0.02, count=floors, **glow(c.dim, 0.6))]
    for i, p in enumerate(P):
        x = (i - (len(P) - 1) / 2) * gapx
        y = f"(var.y{i} - 0.5)*{span}"
        for dx in (-0.36, 0.36):
            layers.append(box(x + dx, 0, 0.2, 0.012, span / 2 + 0.3, 0.02, **glow(c.dim, 0.8)))
        layers.append({"type": "beam", "from": [x, span / 2 + 0.3, 0.1], "to": [x, y, 0.1], "width": 0.012, "glow": 0.5, "samples": 4, "color": c.ink})
        layers.append(box(x, y, 0, 0.27, 0.23, 0.05, **glow(c.col(i), f"0.45 + 1.8*env.h{i}")))
        layers.append(box(x, y, -0.06, 0.012, 0.23, 0.02, **glow("#000000", 1)))
        layers.append(box(x + 0.31, f"0 - {y}", 0.15, 0.03, 0.2, 0.03, **glow(c.ink, 0.5)))
    return {"background": c.bg, "camera": FLAT, "vars": vars_, "env": env, "layers": layers, "filters": [bloom(c, 0.35, 0.016, 0.6)]}


@idiom(needs=1, fam="game", max_cell=24)
def fan(c):
    """A hand of cards, one for each sixteenth of the riff, fanned out: the card of the
    sixteenth now sounding stands up out of the hand."""
    P = [p for p in c.riffs[:2] if p.cell <= 24]
    if not P:
        raise ValueError("too many cards to hold")
    layers = []
    for i, p in enumerate(P):
        n_ = p.cell
        up = 1 if i == 0 else -1
        step = min(0.03, 0.34 / n_)
        a = f"((inst.i - {(n_ - 1) / 2})*{step:g})"
        d = f"(fract({p.turn} - inst.i/{n_})*{n_})"
        R = f"(3.2 + 0.55*exp(0 - 1.1*{d}))"
        py = -3.6 if len(P) == 1 else (-3.75 if up > 0 else 3.75)
        layers.append(box(f"{R}*sin({a})", f"{py} + {up}*{R}*cos({a})", f"0 - inst.i*0.012", 0.36, 0.56, 0.004, rz=f"0 - {up}*{a}", count=n_, **glow("#efe9dc", f"0.55 + 0.45*exp(0 - 1.1*{d})")))
        layers.append(box(f"{R}*sin({a})", f"{py} + {up}*{R}*cos({a})", f"0 - inst.i*0.012 - 0.006", 0.26, 0.44, 0.004, rz=f"0 - {up}*{a}", count=n_, **glow(c.col(i), f"0.25 + 1.6*exp(0 - 1.1*{d})")))
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.3, 0.014, 0.75)]}


@idiom(needs=1, fam="string", max_cell=32)
def switchboard(c):
    """An exchange: sixteen sockets along the top for the sixteenths of the bar, and along
    the bottom one for each sixteenth of the riff. Every note is a cord plugged from where it
    falls in the bar to where it falls in the riff, so the cords lean further over each bar."""
    P = [p for p in c.riffs[:2] if p.cell <= 32]
    if not P:
        raise ValueError("too long a riff for the board")
    A = P[0]
    n_ = A.cell
    dx_t, dx_b = 0.5, min(0.5, 8.0 / n_)
    layers = [box(0, 0, 0.3, 4.4, 2.4, 0.05, **glow("#181512", 1)),
              box(0, 1.75, 0.2, 4.2, 0.02, 0.01, **glow(c.dim, 0.45)),
              box(0, -1.75, 0.2, 4.2, 0.02, 0.01, **glow(c.dim, 0.45)),
              ball(f"(inst.i - 7.5)*{dx_t}", 1.75, 0.1, 0.095, 8, count=16, **glow(c.dim, f"0.75 + 2.4*exp(0 - 2*fract(time.bar - inst.i/16)*16)")),
              ball(f"(inst.i - {(n_ - 1) / 2})*{dx_b:g}", -1.75, 0.1, 0.095, 8, count=n_, **glow(c.dim, f"0.75 + 2.4*exp(0 - 2*fract({A.turn} - inst.i/{n_})*{n_})"))]
    for i, p in enumerate(P):
        keep = max(4, 2 * p.cell / 4)
        x1 = f"(floor({NOTE16}) - 7.5)*{dx_t}"
        x2 = f"(floor(fract((note.beat*4 - {A.anchor:g} + {n_ * 4096})/{n_} + 0.0006)*{n_}) - {(n_ - 1) / 2})*{dx_b:g}"
        layers.append({"type": "beam", "notes": {"track": p.name, "past": keep}, "from": [x1, 1.75, 0], "to": [x2, -1.75, 0], "sag": "0.35 + 0.25*hash(note.i*1.3)", "width": 0.032, "samples": 28,
                       "glow": f"0.75 + 2.0*exp(0 - 2*note.age)", "color": c.col(i), "opacity": f"1 - smooth({keep * 0.6:g}, {keep:g}, note.age)"})
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.35, 0.016, 0.6)]}


@idiom(needs=0, fam="field")
def lava(c):
    """Warm wax: a gout for every note rises from where it fell in the bar, and they run
    into one another as they go up."""
    P = _cast(c, 2)
    layers = [{"type": "shape", "sides": 1, "radius": 0.9, "fill": 1, "width": 0, "color": "#ffffff", "x": f"0.9*sin(time.bar/7)", "y": -1.75, "opacity": 0.6}]
    for i, p in enumerate(P):
        layers.append({"type": "shape", "notes": {"track": p.name, "past": 9}, "sides": 1, "radius": f"(0.07 + 0.1*note.vel)*(1 - 0.6*smooth(4, 9, note.age))", "fill": 1, "width": 0, "color": "#ffffff",
                       "x": f"({NOTE16} - 8)*0.2 + 0.12*sin(note.age/4 + hash(note.i))", "y": f"0 - 1.05 + (0.2 + 0.1*hash(note.i*3.7 + {i}))*note.age", "opacity": 0.5})
    return {"background": "#000000", "layers": layers,
            "filters": [{"type": "blur", "radius": 0.05}, {"type": "posterize", "levels": 6}, {"type": "remap", "gain": 1.25, "palette": [c.bg, c.b, c.a, "#fff3d6"]}, bloom(c, 0.25, 0.02, 0.8)]}


@idiom(needs=1, fam="light")
def searchlights(c):
    """Lights on the ground at night, one for each riff: each sweeps over and back once in
    its turn, so they cross where the riffs do."""
    P = c.riffs[:4]
    layers = [{"type": "stars", "count": 500, "speed": 0, "size": 0.8, "light": 0.5, "twinkle": 0.3, "streak": 0},
              {"type": "shape", "sides": 1, "radius": 0.14, "fill": 1, "width": 0, "color": "#e8e4d4", "x": 1.2, "y": 0.62, "opacity": 0.8}]
    for i, p in enumerate(P):
        x = (i - (len(P) - 1) / 2) * (7.2 / max(len(P), 2))
        th = f"(0.105*sin({p.turn}))"
        layers.append({"type": "beam", "from": [x, -2.35, 0], "to": [f"{x} + 8*sin({th})", f"0 - 2.35 + 8*cos({th})", 0], "width": 0.05, "taper": -7, "glow": f"0.35 + 0.5*{p.hit}", "fade": 0.75, "samples": 60, "color": c.col(i)})
        layers.append(ball(x, -2.3, -0.05, 0.12, 8, **glow(c.col(i), f"1.5 + 3*{p.hit}")))
    layers.append(box(f"(inst.i - 9.5)*0.5", f"0 - 2.6 + 0.25*hash(inst.i*3.3)", -0.1, 0.24, 0.45, 0.02, count=20, **glow("#020203", 1)))
    return {"background": "#03040a", "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.5, 0.03, 0.5)]}


@idiom(needs=1, fam="light", max_cell=32)
def tesla(c):
    """A globe with a stud for each sixteenth of the riff round its rim: every note is a
    spark from the middle to the stud of its sixteenth."""
    P = [p for p in c.riffs[:2] if p.cell <= 32]
    if not P:
        raise ValueError("too many studs")
    layers = [ball(0, 0, 0, 0.26, 12, **glow(c.ink, f"1.2 + 3*{P[0].hit}"))]
    for i, p in enumerate(P):
        n_, R = p.cell, (2.2, 1.3)[i]
        layers.append({"type": "shape", "sides": 0, "radius": R / FH * 1.0, "width": 0.004, "fill": 0, "color": c.dim, "opacity": 0.7})
        layers.append(ball(f"{R}*sin(inst.i/{n_})", f"{R}*cos(inst.i/{n_})", 0, 0.06, 8, count=n_, **glow(c.dim, f"0.6 + 3*exp(0 - 1.5*fract({p.turn} - inst.i/{n_})*{n_})")))
        a = f"(floor({p.nstep} + 0.01)/{n_})"
        for wdt, col, op in ((0.05, c.col(i), 0.8), (0.018, "#ffffff", 1.0)):
            layers.append({"type": "beam", "notes": {"track": p.name, "past": 1.2}, "from": [0, 0, 0], "to": [f"{R}*sin({a})", f"{R}*cos({a})", 0], "width": wdt, "jag": 0.22, "bolt": "floor(time.t*14) + note.i", "samples": 40,
                           "glow": "2.2*exp(0 - 3.5*note.age)", "color": col, "opacity": f"{op}*step(note.age, 1.1)"})
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.6, 0.025, 0.45)]}


@idiom(needs=2, fam="body", cost=2)
def duel(c):
    """Two with foils: each lunges on the notes of a riff of its own, and steel meets only
    where the riffs do."""
    A, B = c.riffs[0], c.riffs[1]
    env = hit_env([A, B], "300ms")
    both = "env.h0*env.h1"
    layers = [lamp(0, 5, -5, 1.4), lamp(0, 1.4, -1.5, 0.6, c.a, 6), floor(c, 0, "#17171b", 0.7), box(0, 0.01, 0, 4.2, 0.01, 0.55, **solid("#2a2a31", 0.6)),
              ball(0, 1.75, -0.2, f"0.02 + 0.3*{both}", 8, **glow("#fff6d0", f"8*{both}"))]
    for i, (p, sgn) in enumerate(((A, -1), (B, 1))):
        e = f"env.h{i}"
        layers.append({"type": "figure", "rig": "human", "motion": "none", "x": f"{sgn}*(1.45 - 0.5*{e})", "y": f"1.3 - 0.12*{e}", "z": 0, "scale": 1.25, "ry": sgn * 0.25, **skin(("#e8e4da", "#3a3d48")[i], 0.05),
                       "extra": [{"name": "foil", "parent": "forearm_r", "length": 0.95, "dir": [0, -1, 0], "width": 0.012}],
                       "pose": {"arm_r": [f"0.17 + 0.08*{e}", 0, 0.02], "forearm_r": [f"0.06 - 0.05*{e}", 0, 0], "arm_l": ["0 - 0.12", 0, -0.06], "forearm_l": [0.2, 0, 0],
                                "thigh_r": [f"0.08 + 0.14*{e}", 0, 0], "shin_r": [f"0 - 0.06 - 0.1*{e}", 0, 0], "thigh_l": [f"0 - 0.05 - 0.1*{e}", 0, 0], "shin_l": ["0 - 0.03", 0, 0], "spine": [f"0.02 + 0.04*{e}", 0, 0]}})
    look = {"background": c.bg, "env": env, "layers": layers, "filters": post3d(0, 5, -5)}
    return shots(c, look, [cam("0.4*sin(time.bar/8)", 1.6, -6.2, look=(0, 1.4, 0), zoom=1.9), cam(-4.6, 1.9, -2.6, look=(0.4, 1.4, 0), zoom=1.7), cam(0, 5.6, -2.8, look=(0, 1.0, 0), zoom=1.7)], A)


@idiom(needs=2, fam="body", cost=2)
def seesaw(c):
    """A plank over a trestle with somebody at each end: each end is sent down by the notes of
    its own riff."""
    A, B = c.riffs[0], c.riffs[1]
    env = hit_env([A, B], "500ms")
    L, h0 = 2.6, 1.0
    th = "(0.045*var.tilt)"
    layers = [{"type": "sky", "zenith": "#31456f", "horizon": c.a, "ground": "#33302a", "sun": "#fff0d0", "sun_yaw": 0.4, "sun_height": 0.09, "sun_size": 0.04, "clouds": 0.15}, floor(c, 0, "#57503f", 0.95),
              {"type": "mesh", "shape": "cone", "detail": 12, "x": 0, "y": h0 / 2, "z": 0, "scale": h0 * 0.52, **solid("#3c4350", 0.6, 0.4)},
              box(0, h0, 0, L + 0.3, 0.04, 0.2, rz=th, **solid("#8a6238", 0.7))]
    for i, sgn in enumerate((-1, 1)):
        x, y = f"{sgn}*{L}*cos({th})", f"{h0} + {sgn}*{L}*sin({th}) + 0.12"
        e = f"env.h{i}"
        layers.append({"type": "figure", "rig": "human", "motion": "none", "x": x, "y": y, "z": 0, "scale": 0.95, "ry": sgn * 0.25, **skin(c.col(i), 0.15),
                       "pose": {"thigh_l": [0.2, 0, 0], "thigh_r": [0.2, 0, 0], "shin_l": [f"0 - 0.1 - 0.1*{e}", 0, 0], "shin_r": [f"0 - 0.1 - 0.1*{e}", 0, 0], "arm_l": [0.16, 0, -0.03], "arm_r": [0.16, 0, 0.03],
                                "forearm_l": [0.12, 0, 0], "forearm_r": [0.12, 0, 0], "spine": [f"0.02 + 0.03*{e}", 0, 0]}})
    look = {"background": "#31456f", "vars": {"tilt": {"follow": "env.h1 - env.h0", "attack": "110ms", "release": "380ms"}}, "env": env, "layers": layers,
            "filters": [{"type": "shadowmap", "amount": 0.6, "soft": 2, "size": 1024}, {"type": "ao", "amount": 0.4, "radius": 0.05}, {"type": "tonemap", "knee": 0.8}, {"type": "aa"}]}
    return shots(c, look, [cam(0, 1.5, -8.2, look=(0, 1.3, 0), zoom=1.9), cam(6.0, 2.2, -5.5, look=(0, 1.2, 0), zoom=1.7), cam(-5.5, 0.7, -3.5, look=(0, 1.4, 0), zoom=1.5)], A)


@idiom(needs=1, fam="body", cost=2, max_cell=40)
def trampoline(c):
    """Somebody on a trampoline for each riff, coming down as it begins each turn: the longer
    the riff, the higher they go."""
    P = c.riffs[:3]
    layers = [lamp(-3, 7, -6, 1.8), lamp(2, 1.8, -4.5, 0.85, c.b, 12), floor(c, 0, "#242630", 0.7)]
    for i, p in enumerate(P):
        x = (i - (len(P) - 1) / 2) * 2.5
        T = p.cell * c.six
        H = max(0.5, min(3.4, 1.25 * T * T))
        u = f"fract({p.turn})"
        up = f"(4*{u}*(1 - {u}))"
        land = f"exp(0 - 14*{u}) + exp(0 - 14*(1 - {u}))"
        layers.append({"type": "mesh", "shape": "cylinder", "detail": 20, "x": x, "y": f"0.42 - 0.07*({land})", "z": 0, "scale": 1, "sx": 0.95, "sy": 0.03, "sz": 0.95, **solid("#323746", 0.45), "emit": 0.08})
        layers.append({"type": "mesh", "shape": "torus", "detail": 20, "tube": 0.06, "x": x, "y": 0.45, "z": 0, "scale": 0.98, **solid(c.col(i), 0.4, 0.35), "emit": f"0.35 + 0.45*({land})"})
        layers.append({"type": "figure", "rig": "human", "motion": "none", "x": x, "y": f"1.42 + {H:g}*{up} - 0.1*({land})", "z": 0, "scale": 1.0, "rx": f"0 - {(0, 1, 0)[(i + c.variant) % 3]}*smooth(0.15, 0.85, {u})",
                       **skin(("#ece7dc", c.col(i), "#d4dce8")[i], 0.16),
                       "pose": {"thigh_l": [f"0.2*{up}", 0, 0], "thigh_r": [f"0.2*{up}", 0, 0], "shin_l": [f"0 - 0.25*{up}", 0, 0], "shin_r": [f"0 - 0.25*{up}", 0, 0],
                                "arm_l": [f"0.1 + 0.3*{up}", 0, -0.05], "arm_r": [f"0.1 + 0.3*{up}", 0, 0.05], "spine": [f"0.05*{up}", 0, 0]}})
    look = {"background": c.bg, "layers": layers, "filters": post3d(-3, 7, -6)}
    return shots(c, look, [cam("0.5*sin(time.bar/9)", 2.2, -9.2, look=(0, 1.55, 0), zoom=1.45), cam(5.8, 1.2, -5.6, look=(0, 1.65, 0), zoom=1.38), cam(-1.0, 0.9, -6.4, look=(0, 1.75, 0), zoom=1.35)], P[0])


@idiom(needs=2, fam="trace", cost=2)
def rink(c):
    """A skater on clean ice: across the rink in time with one riff and along it with the
    other, and the ice keeps the line."""
    A, B = c.riffs[0], c.riffs[1]
    ma, mb = max(1, math.ceil(2.4 / (A.cell * c.six))), max(1, math.ceil(2.4 / (B.cell * c.six)))
    ua, ub = f"({A.turn}/{ma})", f"({B.turn}/{mb})"
    x, z = f"3.3*sin({ua})", f"1.9*sin({ub} + 0.125)"
    face = f"atan2({1 / (A.cell * ma):g}*3.3*cos({ua}), {1 / (B.cell * mb):g}*1.9*cos({ub} + 0.125))"
    layers = [lamp(0, 9, -3, 1.0), lamp(-6, 3, -6, 0.35, "#cfe2ff"),
              {"type": "mesh", "shape": "plane", "detail": 4, "x": 0, "y": 0, "z": 0, "scale": 30, "material": "pbr", "rough": 0.5, "metal": 0.0, "color": "#4f6f8f", "rim": 0, "cull": True},
              box(0, 0.25, 2.6, 4.2, 0.25, 0.06, **solid("#b33a3a", 0.6)), box(0, 0.25, -2.6, 4.2, 0.25, 0.06, **solid("#b33a3a", 0.6)),
              {"type": "trail", "x": x, "y": 0.02, "z": z, "length": f"clamp(scene.t, 0.05, {min(30.0, (c.b16 - c.a16) * c.six):g})", "samples": 900, "width": 0.035, "taper": 0, "glow": 0.9, "fade": 0.3, "color": "#ffffff"},
              {"type": "figure", "rig": "human", "motion": "none", "x": x, "y": 1.4, "z": z, "scale": 1.35, "ry": face, **skin(c.a, 0.25),
               "pose": {"thigh_l": ["0 - 0.14", 0, 0], "shin_l": ["0 - 0.08", 0, 0], "thigh_r": [0.05, 0, 0], "spine": [0.06, 0, 0], "arm_l": [0, 0, -0.17], "arm_r": [0, 0, 0.17]}}]
    look = {"background": "#2c3f55", "layers": layers, "filters": [{"type": "shadowmap", "amount": 0.5, "soft": 2.5, "size": 1024, "sun": 0, "x": 0, "y": 9, "z": -3}, {"type": "ao", "amount": 0.3, "radius": 0.05}, {"type": "tonemap", "knee": 0.8}, {"type": "aa"}]}
    return shots(c, look, [cam(0, 6.5, -6.0, look=(0, 0.3, 0), zoom=1.9), cam(5.5, 2.4, -5.5, look=(0, 0.8, 0), zoom=1.6), cam(0, 10, -0.5, look=(0, 0, 0), zoom=1.9)], A)


@idiom(needs=1, fam="type", max_cell=48)
def specimen(c):
    """A type specimen: one letter of the song's name as big as the frame, the next each
    time the riff comes round; the ink rises up it through the turn."""
    A = c.riffs[0]
    name = _letters(c)
    t0 = math.floor((c.a16 - A.anchor) / A.cell)
    k = f"(floor({A.turn}) - {t0})"
    ph = f"fract({A.turn})"
    n_ = min(A.cell, 32)
    d = f"(fract({A.turn} - inst.i/{n_})*{n_})"
    layers = [{"type": "text", "text": name, "pick": k, "size": 1.5, "x": 0, "y": -0.72, "align": "center", "width": 0.2, "skew": 0, "color": c.ink},
              {"type": "text", "text": name, "pick": f"{k} + 1", "size": 0.3, "x": 1.35, "y": -0.72, "align": "center", "width": 0.16, "skew": 0, "color": c.dim, "opacity": 0.9},
              {"type": "shape", "sides": 4, "rotate": 0.125, "radius": 2.6, "width": 0, "fill": 1, "color": c.a, "blend": "difference", "x": 0, "y": f"0 - 2.838 - 0.74 + 1.5*{ph}"},
              {"type": "shape", "sides": 1, "repeat": n_, "radius": f"0.012 + 0.014*exp(0 - 1.5*{d})", "width": 0, "fill": 1, "color": c.ink, "opacity": f"0.35 + 0.65*exp(0 - 1.5*{d})",
               "x": f"(inst.i - {(n_ - 1) / 2})*{min(0.09, 3.0 / n_):g}", "y": -0.88}]
    return {"background": c.bg, "layers": layers, "filters": [bloom(c, 0.2, 0.012, 0.8)]}


@idiom(needs=1, fam="flock", max_cell=48)
def drill(c):
    """A drill team seen from above: each time the riff comes round they move off into the
    next figure (a ring, a rank, two files, a wedge, a coil), and are in it half a turn later."""
    A = c.riffs[0]
    B = c.riffs[1] if len(c.riffs) > 1 else None
    n_ = 36
    t0 = math.floor((c.a16 - A.anchor) / A.cell)
    per = max(1, math.ceil(1.8 / (A.cell * c.six)))         # a figure lasts at least a couple of seconds
    turn = f"(({A.turn} - {t0})/{per})"
    f = f"floor({turn})"
    u = f"smooth(0, 0.55, fract({turn}))"
    t = f"(inst.i/{n_})"
    forms = [(f"2.1*sin({t})", f"2.1*cos({t})"),
             (f"({t} - 0.5)*7.6", "0"),
             (f"(floor(inst.i/2)/{n_ // 2} - 0.5)*7.2", f"(inst.i - 2*floor(inst.i/2) - 0.5)*1.6"),
             (f"({t} - 0.5)*6.4", f"abs({t} - 0.5)*5.2 - 1.3"),
             (f"(0.5 + 1.9*{t})*sin(2.5*{t})", f"(0.5 + 1.9*{t})*cos(2.5*{t})"),
             (f"(fract(inst.i/6) - 0.42)*6.4", f"(floor(inst.i/6)/6 - 0.42)*3.6")]
    nf = len(forms)

    def pos(axis, which):
        # The figure numbered `which` (wrapped), as a sum over the figures with one weight at 1.
        w = f"fract(({which})/{nf} + 0.001)*{nf}"
        return " + ".join(f"(1 - min(abs(floor({w} + 0.01) - {j}), 1))*({forms[j][axis]})" for j in range(nf))
    x = f"mix({pos(0, f)}, {pos(0, f + ' + 1')}, {u})"
    y = f"mix({pos(1, f)}, {pos(1, f + ' + 1')}, {u})"
    beat = f"exp(0 - 1.5*fract({A.turn} - inst.i/{n_})*{A.cell})"
    line = "#24523a" if c.variant % 2 == 0 else "#3a3660"
    layers = [box(0, 0, 0.3, 4.6, 2.6, 0.05, **glow("#10261a" if c.variant % 2 == 0 else "#1c1a2c", 1)),
              # The parade ground's lines: one every unit across, the halfway line and the touchlines heavier.
              box("(inst.i - 4)*1.0", 0, 0.24, 0.007, 2.45, 0.01, count=9, **glow(line, 0.8)),
              box(0, 0, 0.24, 0.016, 2.45, 0.01, **glow(line, 1.1)),
              box(0, "(inst.i - 0.5)*4.9", 0.24, 4.45, 0.012, 0.01, count=2, **glow(line, 1.1)),
              box("(inst.i - 0.5)*8.9", 0, 0.24, 0.012, 2.45, 0.01, count=2, **glow(line, 1.1)),
              ball(f"({x}) + 0.07", f"({y}) - 0.07", 0.1, 0.1, 6, count=n_, **glow("#000000", 1)),
              ball(x, y, 0, f"0.085 + 0.05*{beat}", 8, count=n_, **glow(c.ink, f"0.8 + 1.5*{beat}"))]
    if B:
        layers.append(ball(x, y, -0.05, f"0.045*step(0.5, fract(inst.i/2))*(1 + {B.hit})", 6, count=n_, **glow(c.b, f"1.5 + 2*{B.hit}")))
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.3, 0.014, 0.7)]}


# ───────────────────────── a twelfth lot: paintings ─────────────────────────

@idiom(needs=1, fam="art", max_cell=48)
def riley(c):
    """Bands of waves across the whole frame, black and white: a swell travels along them
    once for every turn of the riff, and a second riff sets how deep it runs."""
    A = c.riffs[0]
    B = c.riffs[1] if len(c.riffs) > 1 else A
    rows, per = 24, 170
    line = f"floor(inst.i/{per})"
    u = f"(inst.i/{per} - {line})"                      # 0..1 along the line
    waves = max(2, min(7, A.cell // 2))
    depth = f"(0.045 + 0.05*(0.5 + 0.5*sin({B.turn}/2 + {line}/{rows})))"
    y = f"({line} - {(rows - 1) / 2})*0.088 + {depth}*sin({u}*{waves} - {A.turn} + 0.35*sin({line}/{rows} + {A.turn}/3))"
    thick = f"0.014 + 0.016*(0.5 + 0.5*sin({u}*{waves} - {A.turn} + 0.25))"
    ink = c.ink if c.variant % 2 == 0 else c.a
    return {"background": "#08080a", "layers": [{"type": "shape", "repeat": rows * per, "sides": 1, "radius": thick, "width": 0, "fill": 1, "color": ink, "blend": "max", "x": f"({u} - 0.5)*3.62", "y": y}], "filters": []}


@idiom(needs=1, fam="art", max_cell=48)
def vasarely(c):
    """A board of squares over a swelling that wanders with the riffs: across in the time of
    one, up and down in the time of the other, and deeper on every note."""
    A = c.riffs[0]
    B = c.riffs[1] if len(c.riffs) > 1 else A
    cols, rows = 26, 15
    env = hit_env([A], "350ms")
    gx, gy = f"((inst.i - {cols}*floor(inst.i/{cols})) - {(cols - 1) / 2})*0.142", f"(floor(inst.i/{cols}) - {(rows - 1) / 2})*0.142"
    bx, by = f"1.1*sin({A.turn}/2)", f"0.55*sin({B.turn}/2 + 0.125)"
    dx, dy = f"({gx} - {bx})", f"({gy} - {by})"
    swell = f"((0.7 + 0.5*env.h0)*exp(0 - ({dx}*{dx} + {dy}*{dy})*2.6))"
    odd = f"fract((inst.i - {cols}*floor(inst.i/{cols}) + floor(inst.i/{cols}))/2)*2"
    return {"background": "#0a0a10", "env": env,
            "layers": [{"type": "shape", "repeat": cols * rows, "sides": 4, "rotate": f"0.125 + 0.12*{swell}", "radius": f"0.07*(1 + 1.25*{swell})", "width": 0, "fill": 1, "blend": "normal",
                        "palette": [c.a, c.ink, c.b, c.ink], "pos": f"{odd}*0.25 + 0.5*step(0.5, {swell})", "x": f"{bx} + {dx}*(1 + 0.9*{swell})", "y": f"{by} + {dy}*(1 + 0.9*{swell})"}], "filters": []}


@idiom(needs=1, fam="art", paper=True, max_cell=28)
def kandinsky(c):
    """Squares with circles in them, a square for every sixteenth of the riff: the rings of
    the square now sounding swell, and the colours move one ring inward each turn."""
    A = c.riffs[0]
    n_ = A.cell
    r_ = 1 if n_ <= 6 else 2 if n_ <= 12 else 3 if n_ <= 21 else 4
    cols = math.ceil(n_ / r_)
    s_ = min(3.45 / cols, 1.92 / r_)
    reps = max(1, int(1.95 / (s_ * r_)))         # a short riff's row of squares comes again below, a step on
    r_ *= reps
    total = cols * r_ if reps > 1 else n_
    sq = "floor(inst.i/4)"
    ring = "(inst.i - 4*floor(inst.i/4))"
    x = lambda j: f"(({j}) - {cols}*floor(({j})/{cols}) - {(cols - 1) / 2})*{s_:g}"      # noqa: E731
    y = lambda j: f"({(r_ - 1) / 2} - floor(({j})/{cols}))*{s_:g}"                      # noqa: E731
    d = f"(fract({A.turn} - ({sq} + floor({sq}/{cols}))/{n_})*{n_})"
    paints = ["#d6281a", "#f2c21a", "#1b4f9c", "#16171a", "#e8792b", "#2a8a5a", "#ece6d6", "#7a3b8f"]
    layers = [{"type": "shape", "repeat": total, "sides": 4, "rotate": 0.125, "radius": s_ * 0.5 * 1.36, "width": 0, "fill": 1, "blend": "normal", "palette": paints, "pos": "hash(inst.i*3.3 + 1)", "x": x("inst.i"), "y": y("inst.i")},
              {"type": "shape", "repeat": total * 4, "sides": 1, "radius": f"{s_ * 0.46:g}*(1 - {ring}*0.23)*(1 + 0.07*exp(0 - 1.2*{d}))", "width": 0, "fill": 1, "blend": "normal", "palette": paints,
               "pos": f"hash({sq}*7.1 + ({ring} + floor({A.turn}))*1.3)", "x": x(sq), "y": y(sq)}]
    return {"background": "#ece6d6", "layers": layers, "filters": [{"type": "grain", "amount": 0.05}]}


@idiom(needs=1, fam="art", paper=True)
def suprematist(c):
    """Bars and blocks on a white ground, one for each part: each slides along its own slant
    once over and back in a turn, and jumps on its notes."""
    P = _cast(c, 6)
    env = hit_env(P, "300ms")
    paints = ("#16171a", "#d6281a", "#1b4f9c", "#f2c21a", "#16171a", "#e8792b")
    layers = [box(0, 0, 0.3, 4.6, 2.6, 0.01, **glow("#ece6d6", 1)), box(-1.5 + 3.0 * c.r(40), 0.9 - 1.6 * c.r(41), 0.2, 0.85, 0.85, 0.01, rz=f"0.03 + 0.03*sin(time.bar/6)", **glow("#16171a", 1)),
              ball(f"{2.6 - 5.0 * c.r(42):.3f} + 0.35*sin(time.bar/4)", f"{-1.2 + 2.2 * c.r(43):.3f} + 0.25*cos(time.bar/5)", 0.15, "0.42 + 0.06*audio.low", 14, **glow("#d6281a", 1))]
    for i, p in enumerate(P):
        tilt = (c.r(i + 50) - 0.5) * 0.3
        long_, wide = 0.6 + 1.6 * c.r(i + 60), 0.06 + 0.22 * c.r(i + 70)
        ox, oy = (i - (len(P) - 1) / 2) * (7.0 / len(P)) + (c.r(i + 80) - 0.5) * 1.2, (c.r(i + 90) - 0.5) * 3.4
        slide = f"(1.45*sin({p.turn}/2) + 0.45*env.h{i})" if p.cell else f"0.65*env.h{i}"
        layers.append(box(f"{ox:.3f} + {math.cos(tilt * 6.2832):.4f}*{slide}", f"{oy:.3f} + {math.sin(tilt * 6.2832):.4f}*{slide}", 0.1 - 0.02 * i, f"{long_:.3f}*(1 + 0.16*env.h{i})", wide, 0.01, rz=f"{tilt:.3f} + 0.025*env.h{i}", **glow(paints[i], 1)))
    return {"background": "#ece6d6", "env": env, "camera": FLAT, "layers": layers, "filters": [{"type": "grain", "amount": 0.05}]}


@idiom(needs=1, fam="art")
def rothko(c):
    """Two or three fields of colour, one over another, their edges soft: each belongs to a
    part and breathes with it."""
    P = _cast(c, 3)
    env = hit_env(P, "1200ms")
    n_ = len(P)
    layers = [box(0, 0, 0.3, 4.6, 2.6, 0.01, **glow(c.bg, 1))]
    top = 2.2
    share = [(1.6, 2.4), (1.0, 1.9, 1.3), (0.9, 1.5, 1.0, 0.8)][min(n_, 3) - 1]
    for i, p in enumerate(P):
        h = share[i]
        swell = f"(1 + 0.06*env.h{i} + 0.03*sin({p.turn}/2))" if p.cell else f"(1 + 0.06*env.h{i})"
        layers.append(box(0, top - h / 2, 0.1, f"3.9*{swell}", f"{h / 2 - 0.12:g}*{swell}", 0.01, **glow(c.col(i), f"0.75 + 0.5*env.h{i}")))
        top -= h
    return {"background": c.bg, "env": env, "camera": FLAT, "layers": layers, "filters": [{"type": "blur", "radius": 0.022}, {"type": "grain", "amount": 0.06}]}


@idiom(needs=2, fam="art", max_cell=64)
def albers(c):
    """Squares one inside another, one for each riff, the outermost the slowest: each takes
    its next colour when its riff comes round, and gives a little on its notes."""
    P = sorted(c.riffs[:4], key=lambda p: -p.cell)
    env = hit_env(P, "300ms")
    paints = [c.a, c.b, c.c, c.ink, c.dim, c.a]
    layers = []
    for i, p in enumerate(P):
        size = 2.35 * (0.74 ** i)
        t0 = math.floor((c.a16 - p.anchor) / p.cell)
        layers.append(box(0, f"0 - {0.11 * i:g}", 0.3 - 0.05 * i, f"{size:g}*(1 + 0.03*env.h{i})", f"{size:g}*(1 + 0.03*env.h{i})", 0.01, palette=paints, pos=f"fract((floor({p.turn}) - {t0} + {i * 2})/6)", emit=1, light=0, ambient=1, rim=0))
    return {"background": c.bg, "env": env, "camera": FLAT, "layers": layers, "filters": [{"type": "grain", "amount": 0.05}]}


# ───────────────────────── a thirteenth lot: sand, ink and shadow ─────────────────────────

def _grey(g):
    v = max(0, min(255, int(g * 255)))
    return f"#{v:02x}{v:02x}{v:02x}"


@idiom(needs=0, fam="field")
def marbling(c):
    """Marbled paper: every note lets a drop of colour fall on the bath, where it came in its
    riff and as high as it was sung, and the bath is slowly combed."""
    P = _cast(c, 3)
    layers = []
    # Seed a few soft ambient base drops so the bath is already swirled from frame 0 even in sparse passages.
    layers.append({"type": "shape", "repeat": 6, "sides": 1, "radius": "0.14 + 0.05*sin(time.beat*0.4 + inst.i*1.3)", "width": 0, "fill": 1, "blend": "max",
                   "color": _grey(0.55), "x": "0 - 1.35 + inst.i*0.54 + 0.2*sin(time.beat*0.25 + inst.i)", "y": "0.45*cos(time.beat*0.2 + inst.i*1.7)"})
    for i, p in enumerate(P):
        layers.append({"type": "shape", "notes": {"track": p.name, "past": 1.2}, "sides": 1, "radius": "(0.05 + 0.1*note.vel)*smooth(0 - 0.05, 0.5, note.age)", "width": 0, "fill": 1, "blend": "max",
                       "color": _grey((1.0, 0.72, 0.5)[i]), "x": f"({p.nph} - 0.5)*3.1", "y": p.pitch(-0.78, 0.78)})
    inks = [["#efe6d0", c.b, "#efe6d0", c.a, "#1c1a22", c.c], ["#f1ead8", "#1f4e79", "#f1ead8", "#b23a2a", "#e0a526", "#1c1a22"], ["#11131c", c.a, "#f1ead8", c.b, "#11131c", c.c]][c.variant % 3]
    return {"background": "#000000", "layers": layers,
            "filters": [{"type": "flow", "speed": 0.1, "decay": 18, "scale": 2.0 + (c.seed % 3) * 0.5, "change": 0.1}, {"type": "blur", "radius": 0.016}, {"type": "posterize", "levels": 6},
                        {"type": "remap", "palette": inks}, {"type": "grain", "amount": 0.05}]}


@idiom(needs=0, fam="fall")
def ink(c):
    """Ink let fall into water: a drop for every note, where it came in the bar; each sinks,
    and curls as it goes."""
    P = _cast(c, 2)
    layers = []
    for i, p in enumerate(P):
        layers.append({"type": "shape", "notes": {"track": p.name, "past": 0.5}, "sides": 1, "radius": "0.016 + 0.035*note.vel", "width": 0, "fill": 1, "blend": "max", "color": _grey((1.0, 0.55)[i]),
                       "x": f"({NOTE16} - 7.5)*0.21", "y": f"{0.93 - 0.25 * i:g} - 0.3*note.age"})
    return {"background": "#000000", "layers": layers,
            "filters": [{"type": "flow", "field": "fall", "speed": 0.2, "decay": 12}, {"type": "flow", "speed": 0.1, "decay": 12, "scale": 3, "change": 0.18}, {"type": "blur", "radius": 0.004},
                        {"type": "remap", "gain": 1.15, "palette": ["#efe8d6", "#efe8d6", c.b, "#15151c", "#08080c"]}, {"type": "grain", "amount": 0.05}]}


@idiom(needs=1, fam="count", max_cell=64)
def hourglass(c):
    """A sand glass for each riff: it runs out in exactly one turn, and is turned over as the
    riff comes round."""
    P = c.riffs[:3]
    env = hit_env(P, "220ms")
    R = (0.58, 0.45, 0.31)[len(P) - 1]
    UP = 0.0              # the turn of a three-sided shape that stands on its base
    layers = []
    for i, p in enumerate(P):
        cx = (i - (len(P) - 1) / 2) * (1.45 if len(P) < 3 else 1.1)
        ph = f"fract({p.turn})"
        th = f"(0.5*smooth(0.86, 1, {ph}))"                 # turned over through the last of the turn
        at = lambda ly: (f"{cx:g} - ({ly})*sin({th})", f"({ly})*cos({th})")            # noqa: E731
        rt, rb = f"({R * 0.9:g}*sqrt(1 - {ph}))", f"({R * 0.9:g}*sqrt({ph}))"
        col = c.col(i)
        for ly, r, rot_, kw in ((f"{R:g}", R, 0.5, {"width": 0.007, "fill": 0, "color": c.ink}), (f"0 - {R:g}", R, 0.0, {"width": 0.007, "fill": 0, "color": c.ink}),
                                (rt, rt, 0.5, {"width": 0, "fill": 1, "color": col, "opacity": f"0.75 + 0.25*env.h{i}"}),
                                (f"{rb}/2 - {1.5 * R:g}", rb, 0.0, {"width": 0, "fill": 1, "color": col, "opacity": f"0.75 + 0.25*env.h{i}"})):
            x, y = at(ly)
            layers.append({"type": "shape", "sides": 3, "radius": r, "rotate": f"{UP + rot_:g} + {th}", "x": x, "y": y, "blend": "max", **kw})
        # The thread of sand, brighter on the riff's notes.
        layers.append({"type": "shape", "repeat": 7, "sides": 1, "radius": f"0.007 + 0.006*env.h{i}", "width": 0, "fill": 1, "color": col, "x": cx,
                       "y": f"0 - fract(time.beat*1.5 + inst.i/7)*({1.5 * R:g} - 1.5*{rb})", "opacity": f"1 - step(0.86, {ph})"})
        # Its frame: a bar above and below.
        for ly in (1.5 * R + 0.03, -1.5 * R - 0.03):
            x, y = at(f"{ly:g}")
            layers.append({"type": "shape", "repeat": 9, "sides": 1, "radius": 0.016, "width": 0, "fill": 1, "color": c.dim, "x": f"{x} + (inst.i - 4)*{R * 0.215:g}*cos({th})", "y": f"{y} + (inst.i - 4)*{R * 0.215:g}*sin({th})"})
    return {"background": c.bg, "env": env, "layers": layers, "filters": [bloom(c, 0.3, 0.016, 0.6)]}


@idiom(needs=1, fam="game", cost=2, max_cell=40)
def hanoi(c):
    """The tower puzzle: a disc is moved on every sixteenth, and the whole tower is carried
    across once in a turn of the riff (a riff of seven is three discs exactly; a longer one
    has the tower wait for it)."""
    A = c.riffs[0]
    q = 1 if A.cell >= 7 else 2 if A.cell >= 4 else 3          # a short riff takes two or three turns over it
    span = A.cell * q
    n_ = max(2, min(5, int(math.log2(span + 1))))
    per = 2 ** n_ - 1
    s = f"floor(fract({A.turn}/{q})*{span} + 0.001)"
    D, th = 2.3, 0.27
    tx, ty = max(20, int(300 * c.six)), max(10, int(140 * c.six))
    vars_ = {"m": {"follow": f"(floor({A.turn}/{q}) + 64)*{per + 1} + min({s} + 1, {per})", "attack": "0ms", "release": "0ms"}}
    for k in range(n_):
        vars_[f"p{k}"] = {"follow": f"floor(fract({1 if k % 2 == 0 else 2}*floor((var.m + {2 ** k})/{2 ** (k + 1)})/3)*3 + 0.5)", "attack": "0ms", "release": "0ms"}
    for k in range(n_):
        under = " + ".join(f"(1 - step(0.5, abs(var.p{j} - var.p{k})))" for j in range(k + 1, n_)) or "0"
        vars_[f"x{k}"] = {"follow": f"(var.p{k} - 1)*{D}", "attack": f"{tx}ms", "release": f"{tx}ms"}
        vars_[f"y{k}"] = {"follow": f"mix({th}*({under} + 0.5), 2.0, min(1, abs((var.p{k} - 1)*{D} - var.x{k})/{0.3 * D:g}))", "attack": f"{ty}ms", "release": f"{ty}ms"}
    wood = solid("#6b4a2a", 0.55)
    layers = [lamp(-3, 6, -5, 1.4), lamp(4, 2.5, -4, 0.5, c.b), floor(c, -0.12, "#17171b", 0.6), box(0, -0.06, 0, 3.7, 0.06, 1.15, **wood)]
    for x in (-D, 0, D):
        layers.append({"type": "mesh", "shape": "cylinder", "detail": 12, "x": x, "y": 0.85, "z": 0, "scale": 1, "sx": 0.06, "sy": 0.85, "sz": 0.06, **wood})
    cols = [c.a, c.b, c.c, c.ink, "#d8b25a"]
    for k in range(n_):
        r = 0.4 + 0.55 * k / max(n_ - 1, 1)
        moving = f"min(1, abs((var.p{k} - 1)*{D} - var.x{k})*3)"
        layers.append({"type": "mesh", "shape": "cylinder", "detail": 28, "x": f"var.x{k}", "y": f"var.y{k}", "z": 0, "scale": 1, "sx": r, "sy": th / 2 - 0.012, "sz": r, **solid(cols[k % 5], 0.4), "emit": f"0.15 + 0.9*{moving}"})
    look = {"background": c.bg, "vars": vars_, "layers": layers, "filters": post3d(-3, 6, -5)}
    return shots(c, look, [cam("1.2*sin(time.bar/9)", 2.5, -7.4, look=(0, 0.8, 0), zoom=2.2), cam(0, 7.5, -2.2, look=(0, 0.4, 0), zoom=2.0), cam(-6.5, 1.6, -3.0, look=(0, 0.8, 0), zoom=1.9)], A, secs=4.5)


@idiom(needs=1, fam="game", max_cell=24)
def breakout(c):
    """A wall with a course of bricks for each riff, as many as it has sixteenths: a ball
    knocks one out on every sixteenth, and the course is built again when the riff comes round."""
    P = c.riffs[:4]
    layers = []
    for i, p in enumerate(P):
        n_ = p.cell
        w = 8.3 / n_
        y = 1.85 - 0.5 * i
        u = f"(fract({p.turn})*{n_})"
        d = f"(fract({p.turn} - inst.i/{n_})*{n_})"
        there = f"step({u}, inst.i)"
        col = c.col(i)
        layers.append(box(f"(inst.i - {(n_ - 1) / 2})*{w:g}", y, 0, w / 2 - 0.05, 0.18, 0.01, count=n_, **glow(col, f"0.85 + 1.5*exp(0 - 5*{d})*(1 - {there})"), opacity=f"{there} + (1 - {there})*(0.16 + 0.84*exp(0 - 3.5*{d}))"))
        bx = f"(({u} - {(n_ - 1) / 2})*{w:g})"
        by = f"({-2.0 + 0.0 * i:g} + {y + 2.0 - 0.3:g}*abs(cos({u}/2)))"
        layers.append(ball(bx, by, -0.05, 0.09, 10, **glow("#ffffff" if i == 0 else col, 1.3)))
        layers.append(box(bx, -2.22 - 0.07 * i, 0, 0.42, 0.035, 0.01, **glow(col, 0.9)))
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.35, 0.016, 0.7)]}


@idiom(needs=1, fam="body", cost=2)
def shadowplay(c):
    """Shadow puppets against a lit cloth: one for each part, and each moves on its own notes."""
    P = _cast(c, 3)
    env = hit_env(P, "330ms")
    black = {"color": "#0b0705", "emit": 0, "light": 0, "ambient": 1, "rim": 0, "melt": 0.05}
    warm = [["#fff0c0", "#f8bd5c", "#b9581a", "#2a1006"], ["#f4f0ff", "#b9c6f2", "#4a5a9c", "#0a0c1e"], ["#ffe4d6", "#f28a6a", "#8f2a3a", "#1e060c"]][c.variant % 3]
    layers = [{"type": "gradient", "palette": warm, "radial": 1, "x": 0, "y": 0.1, "spread": 0.8, "res": 0.5}]
    for i, p in enumerate(P):
        x = (i - (len(P) - 1) / 2) * 2.4
        e = f"env.h{i}"
        lean = f"0.03*sin({p.turn})" if p.cell else "0"
        pose = [{"arm_r": [f"0.22*{e}", 0, f"0.1 + 0.25*{e}"], "arm_l": [0.02, 0, f"0 - 0.1 - 0.1*{e}"], "forearm_r": [f"0.12*{e}", 0, 0], "head": [f"0 - 0.05*{e}", 0, 0], "spine": [lean, 0, 0]},
                {"arm_l": [f"0.2*{e}", 0, f"0 - 0.12 - 0.3*{e}"], "arm_r": [f"0.2*{e}", 0, f"0.12 + 0.3*{e}"], "thigh_l": [f"0.1*{e}", 0, 0], "shin_l": [f"0 - 0.16*{e}", 0, 0], "spine": [lean, 0, 0]},
                {"arm_r": [0.05, 0, f"0.3 - 0.2*{e}"], "arm_l": [0.05, 0, f"0 - 0.3 + 0.2*{e}"], "thigh_r": [f"0.14*{e}", 0, 0], "shin_r": [f"0 - 0.2*{e}", 0, 0], "head": [f"0.06*{e}", 0, 0], "spine": [lean, 0, 0]}][i]
        layers.append({"type": "figure", "rig": "human", "motion": "none", "x": x, "y": f"1.28 + 0.1*{e}", "z": 0, "scale": 1.3, "ry": (0.12, -0.12, 0.0)[i] if len(P) > 1 else 0, "pose": pose, **black})
        layers.append(box(x, -0.6, 0.05, 0.02, 1.2, 0.02, **{k_: v for k_, v in black.items() if k_ != "melt"}))
    layers.append(box(0, -0.38, -0.2, 6, 0.4, 0.05, **{k_: v for k_, v in black.items() if k_ != "melt"}))
    return {"background": warm[1], "env": env, "camera": cam(0, 1.15, -9, look=(0, 1.15, 0), zoom=2.5), "layers": layers,
            "filters": [{"type": "blur", "radius": 0.003}, {"type": "vignette", "amount": 0.5}, {"type": "grain", "amount": 0.07}]}


@idiom(needs=1, fam="light", max_cell=16)
def candles(c):
    """Candles in a row, one for each sixteenth of the riff: each is lit afresh as its
    sixteenth comes, and burns lower until it comes again. A second riff has the row behind."""
    P = c.riffs[:2]
    layers = []
    for i, p in enumerate(P):
        n_ = p.cell
        gap = min(1.25, 8.3 / n_) * (1 - 0.15 * i)
        k = min(1.0, gap / 0.7) * (1 - 0.15 * i)
        d = f"(fract({p.turn} - inst.i/{n_})*{n_})"
        burn = f"(0.32 + 0.68*exp(0 - 0.42*{d}))"
        y0 = -2.3 + 1.7 * i
        x = f"(inst.i - {(n_ - 1) / 2})*{gap:g}"
        h = f"(0.72 - 0.35*{d}/{n_})*{k:g}"
        layers.append(box(x, f"{y0:g} + {h}", 0.1 + 0.1 * i, 0.14 * k, h, 0.02, count=n_, **glow(_grey(0.32), 1)))
        layers.append(ball(x, f"{y0:g} + 2*{h} + {0.16 * k:g} + {0.1 * k:g}*{burn}", 0.1 * i, f"{0.11 * k:g} + {0.15 * k:g}*{burn}", 10, sy=1.55, count=n_, **glow("#ffffff", f"0.55 + 0.7*{burn}")))
    return {"background": "#000000", "camera": FLAT, "layers": layers,
            "filters": [{"type": "flow", "field": "rise", "speed": 0.34, "decay": 0.65}, {"type": "blur", "radius": 0.005},
                        {"type": "remap", "gain": 1.35, "palette": ["#050308", "#350d08", "#a4260a", "#ea7014", "#fbc036", "#fff6d2"]}, bloom(c, 0.45, 0.02, 0.65)]}


@idiom(needs=1, fam="light", cost=2, max_cell=32)
def sundial(c):
    """A dial with as many hours as the riff has sixteenths, and a sun that goes round it once
    a turn: the shadow of the pin tells the place in the riff."""
    A = c.riffs[0]
    n_ = A.cell
    sx, sz = f"5.2*cos({A.turn} + 0.5)", f"5.2*sin({A.turn} + 0.5)"
    d = f"(fract({A.turn} - inst.i/{n_})*{n_})"
    stone = solid("#a89c80", 0.9)
    layers = [lamp(sx, 3.0, sz, 0.95, "#fff0d0", 30), lamp(0, 8, 0, 0.25, "#cfd8ff"), floor(c, 0, "#5f5a4c", 0.95),
              {"type": "mesh", "shape": "cylinder", "detail": 48, "x": 0, "y": 0.05, "z": 0, "scale": 1, "sx": 2.5, "sy": 0.05, "sz": 2.5, **stone},
              {"type": "mesh", "shape": "cone", "detail": 16, "x": 0, "y": 0.75, "z": 0, "scale": 1, "sx": 0.1, "sy": 0.65, "sz": 0.1, **solid("#7a6a3a", 0.35, 0.8)},
              ball(f"2.05*cos(inst.i/{n_})", 0.14, f"2.05*sin(inst.i/{n_})", 0.12, 10, count=n_, **solid(c.a, 0.5), emit=f"0.25 + 2.2*exp(0 - 1.5*{d})")]
    for i, p in enumerate(c.riffs[1:3]):
        d2 = f"(fract({p.turn} - inst.i/{p.cell})*{p.cell})"
        layers.append(ball(f"{1.55 - 0.4 * i:g}*cos(inst.i/{p.cell})", 0.12, f"{1.55 - 0.4 * i:g}*sin(inst.i/{p.cell})", 0.075, 8, count=min(p.cell, 64), **solid(c.col(i + 1), 0.5), emit=f"0.25 + 2.2*exp(0 - 1.5*{d2})"))
    look = {"background": "#2a2a30", "layers": layers, "filters": post3d(sx, 3.0, sz, shadow=0.85)}
    return shots(c, look, [cam(0, 6.8, -4.6, look=(0, 0, 0.2), zoom=2.0), cam(0, 9.5, -0.6, look=(0, 0, 0), zoom=2.3), cam(-4.5, 3.0, -4.5, look=(0, 0.2, 0), zoom=1.9)], A, secs=5)


@idiom(needs=1, fam="ground", cost=2, max_cell=32)
def zen(c):
    """Raked sand: a stone for each riff with as many rings round it as the riff has
    sixteenths, raked outward through one turn and smoothed away through the next."""
    P = c.riffs[:3]
    spots = [(-0.4, 0.05), (0.36, -0.2), (0.08, 0.46)][:len(P)]
    R = 0.36
    disp, mask = [], []
    layers = [lamp(-6, 1.7, 3, 0.95, "#fff0d8", 40), lamp(3, 5, -4, 0.18, "#cfd8ff")]
    for i, (p, (px, pz)) in enumerate(zip(P, spots)):
        dd = f"len(vtx.x - {px:g}, vtx.z - {pz:g})"
        out = f"({R:g}*(0.5 + 0.5*{_zig(p.turn + '/2')}))"
        m = f"(1 - smooth({out} - 0.02, {out}, {dd}))"
        disp.append(f"0.0065*sin({dd}*{p.cell / R:g})*{m}")
        mask.append(m)
        layers.append(ball(px * 5, 0.1, pz * 5, 0.3 + 0.07 * i, 12, sy=0.62, **solid(("#3b3b40", "#4a443c", "#2f3438")[i], 0.85)))
        layers.append(ball(f"{px * 5:g} + 5*{out}*cos({p.turn})", 0.06, f"{pz * 5:g} + 5*{out}*sin({p.turn})", 0.06, 8, **glow(c.col(i), 1.2)))
    rest = " - ".join(["1"] + [f"min({m}, 1)" for m in mask])
    disp.append(f"0.004*sin(vtx.z*30 + 2*sin(vtx.x*1.5))*max({rest}, 0)")
    layers.insert(2, {"type": "mesh", "shape": "plane", "detail": 170, "x": 0, "y": 0, "z": 0, "scale": 5, "material": "pbr", "rough": 0.95, "metal": 0, "color": "#b3a688", "rim": 0, "displace": " + ".join(disp), "shading": "pixel", "cull": True})
    look = {"background": "#1c1c20", "layers": layers, "filters": post3d(-6, 1.7, 3, shadow=0.8, ao=0.3)}
    return shots(c, look, [cam("2.5*sin(time.bar/14)", 4.4, -5.6, look=(0, 0, 0.3), zoom=1.9), cam(0, 9, -0.5, look=(0, 0, 0), zoom=2.1), cam(-4.2, 1.6, -3.4, look=(0.4, 0, 0.6), zoom=1.7)], P[0], secs=5)


# ───────────────────────── a fourteenth lot: what the songs are about ─────────────────────────

@idiom(needs=2, fam="count", max_cell=96)
def measure(c):
    """The old way to the common measure of two lengths: an oblong as wide as one riff and as
    tall as the other, and the greatest square taken from it, again and again, until what is
    left is itself a square. A lamp goes over it a sixteenth along and a sixteenth up at a
    time and lights the square it is in."""
    E = getattr(c, "euclid", None)
    if E:
        # The song itself takes the less from the greater, section by section: the whole
        # oblong stands, the squares already taken are lit, and the lamp goes over what is left.
        W, H, cut, A, B = E
    else:
        A, B = sorted(c.riffs[:2], key=lambda p: -p.cell)
        if A.cell == B.cell:
            raise ValueError("measure: two riffs of one length")
        W, H, cut = A.cell, B.cell, None
    u = min(8.3 / W, 4.5 / H)
    sq, x0, y0, w, h, stage, wide = [], 0, 0, W, H, 0, True
    while w > 0 and h > 0 and len(sq) < 48:
        if (w >= h) != wide:
            stage, wide = stage + 1, w >= h
        if w >= h:
            sq.append((x0, y0, h, stage))
            x0, w = x0 + h, w - h
        else:
            sq.append((x0, y0, w, stage))
            y0, h = y0 + w, h - w
    if cut is None:
        X, Y = f"(fract({A.turn})*{W})", f"(fract({B.turn})*{H})"
    else:
        # What is left after `cut` squares have been taken: the lamp keeps to it.
        rx, ry, rw, rh = 0, 0, W, H
        for sx_, sy_, s_, _ in sq[:cut]:
            if rw >= rh:
                rx, rw = rx + s_, rw - s_
            else:
                ry, rh = ry + s_, rh - s_
        X, Y = f"({rx} + fract({A.turn})*{rw})", f"({ry} + fract({B.turn})*{rh})"
    cols = [c.a, c.b, c.c, c.ink]
    layers = [box(0, 0, 0.3, W * u / 2 + 0.06, H * u / 2 + 0.06, 0.01, **glow(c.dim, 0.5))]
    for q, (sx_, sy_, s_, st) in enumerate(sq):
        inside = f"step({sx_}, {X})*step({X}, {sx_ + s_})*step({sy_}, {Y})*step({Y}, {sy_ + s_})"
        lit = f"0.32 + 0.68*{inside}" if cut is None else ("0.85" if q < cut else f"{0.34 if q == cut else 0.14} + 0.75*{inside}")
        layers.append(box((sx_ + s_ / 2 - W / 2) * u, (sy_ + s_ / 2 - H / 2) * u, 0.1, s_ * u / 2 - 0.035, s_ * u / 2 - 0.035, 0.01, **glow(cols[(q if cut is not None else st) % 4], lit)))
    last = sq[-1][2]
    if cut is not None and cut >= len(sq) - 1 and W % last == 0 and H % last == 0 and (W // last) * (H // last) <= 400:
        # What is left is a square: the measure is found. It is laid over the whole oblong,
        # as many times as it goes, and a wave crosses the tiles on every beat.
        cols_, rows_ = W // last, H // last
        col, row = f"(inst.i - {cols_}*floor(inst.i/{cols_}))", f"floor(inst.i/{cols_})"
        wave = f"exp(0 - 4*fract(time.beat - ({col} + {row})/{cols_ + rows_}))"
        layers.append(box(f"(({col} + 0.5)*{last} - {W / 2})*{u:g}", f"(({row} + 0.5)*{last} - {H / 2})*{u:g}", -0.05, last * u / 2 * 0.62, last * u / 2 * 0.62, 0.01, count=cols_ * rows_,
                          **glow("#ffffff", f"0.12 + 1.5*{wave}")))
    layers.append(ball(f"({X} - {W / 2})*{u:g}", f"({Y} - {H / 2})*{u:g}", -0.1, max(0.06, min(0.14, 0.3 * u)), 10, **glow("#ffffff", 1.6)))
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.35, 0.016, 0.75)]}


@idiom(needs=0, fam="place")
def courses(c):
    """A wall going up in courses, one for each part: every note is a brick as long as the
    wait for the next one, laid as it sounds, and the wall goes by a sixteenth at a time."""
    P = _cast(c, 7)
    u = 0.19
    rowh = min(0.66, 4.7 / len(P))
    bricks = ["#b5533a", "#a2452e", "#c0623f", "#8f3a26", "#b86a48"]
    layers = [box(0, 0, 0.3, 4.6, 2.6, 0.01, **glow("#2a211c", 1))]
    for i, p in enumerate(P):
        y = (len(P) - 1) / 2 * rowh - i * rowh
        long_ = f"(min(min(note.gap, note.age), 6)*4*{u})"
        layers.append(box(f"3.7 - note.age*4*{u} + {long_}/2", y, 0, f"max({long_}/2 - 0.03, 0.012)", rowh / 2 - 0.035, 0.01, notes={"track": p.name, "past": 10.5}, palette=bricks, pos=f"hash(note.i*1.7 + {i})",
                          emit=f"0.75 + 1.6*exp(0 - 3*note.age)", light=0, ambient=1, rim=0))
    layers.append(box(3.72, 0, -0.05, 0.012, 2.6, 0.01, **glow(c.ink, 0.8)))
    return {"background": "#2a211c", "camera": FLAT, "layers": layers, "filters": [{"type": "grain", "amount": 0.06}, bloom(c, 0.25, 0.014, 0.85)]}


def _walk(n, cap=48):
    """A number walked down to one: halved if even, trebled and one more if odd."""
    out = [n]
    while n != 1 and len(out) < cap:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        out.append(n)
    return out


@idiom(needs=1, fam="tree", max_cell=64)
def hailstone(c):
    """Halve it if it is even; treble it and add one if it is odd. The walks of the first
    sixteen numbers down to one, drawn as one tree, with the walk of the riff's own length
    lit on it and a lamp that goes one step down the walk each time the riff comes round."""
    A = c.riffs[0]
    mine = _walk(max(A.cell, 2))
    walks = [_walk(k) for k in range(2, 17)] + [mine]
    if mine[-1] != 1:
        raise ValueError("hailstone: too long a walk")
    # A number stands as far along as it has steps still to go, and as high as it is big.
    left, edges = {1: 0}, {}
    for w in walks:
        for d_, n_ in enumerate(w[::-1]):
            left[n_] = d_
        for a, b in zip(w, w[1:]):
            edges[(b, a)] = True
    far, top = max(left.values()), max(math.log2(n_) for n_ in left)
    at = lambda n_: ((0.5 - left[n_] / far) * 8.3, (math.log2(n_) / top - 0.5) * 4.4)                 # noqa: E731
    pos = left
    on = {b: j for j, b in enumerate(mine)}                      # a number's place on the riff's walk
    steps = len(mine)
    here = f"(fract(floor({A.turn})/{steps} + 0.0005)*{steps})"   # which step of the walk the lamp is on
    layers = []
    for (a, b) in edges:
        (x1, y1), (x2, y2) = at(a), at(b)
        lit = b in on and a in on
        glow_ = f"0.7 + 1.8*exp(0 - 0.8*abs({on[b]} - {here}))" if lit else 0.75
        layers.append({"type": "beam", "from": [x1, y1, 0], "to": [x2, y2, 0], "width": 0.045 if lit else 0.022, "samples": 12, "glow": glow_, "color": c.a if lit else c.dim})
    for n_ in pos:
        x, y = at(n_)
        if n_ in on:
            layers.append(ball(x, y, -0.05, f"0.075 + 0.11*exp(0 - 1.5*abs({on[n_]} - {here}))", 8, **glow("#ffffff" if n_ != 1 else c.b, f"0.6 + 1.2*exp(0 - 1.5*abs({on[n_]} - {here}))")))
        else:
            layers.append(ball(x, y, -0.05, 0.055, 6, **glow(c.ink, 0.7)))
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.45, 0.018, 0.6)]}


@idiom(needs=2, fam="light", max_cell=64)
def strobe(c):
    """Two wheels in the dark, each turning once in its own riff and seen only by the flash
    of the other's notes: where its hand is caught, time after time, is how the two riffs
    lie against one another."""
    A, B = c.riffs[0], c.riffs[1]
    env = hit_env([A, B], "180ms")
    layers = []
    for i, p in enumerate((A, B)):
        other = 1 - i
        cx, R = (-0.86, 0.86)[i], 0.62
        held = f"(0.25 - ({p.turn} - env.h{other}.age*time.bpm*8/{p.cell}))"          # where the hand was when the flash came
        flash = f"env.h{other}"
        col = c.col(i)
        n_ = min(p.cell, 48)
        layers.append({"type": "shape", "repeat": n_, "sides": 1, "radius": 0.015, "width": 0, "fill": 1, "color": c.dim, "x": f"{cx} + {R + 0.07}*cos(inst.i/{n_} + 0.25)", "y": f"{R + 0.07}*sin(inst.i/{n_} + 0.25)", "opacity": 0.9})
        layers.append({"type": "shape", "repeat": 14, "sides": 1, "radius": "0.016 + 0.014*inst.i/14", "width": 0, "fill": 1, "color": col, "x": f"{cx} + {R}*(inst.i/13)*cos({held})", "y": f"{R}*(inst.i/13)*sin({held})", "opacity": f"0.14 + 0.86*{flash}"})
        layers.append({"type": "shape", "sides": 1, "radius": 0.06, "width": 0, "fill": 1, "color": "#ffffff", "x": f"{cx} + {R}*cos({held})", "y": f"{R}*sin({held})", "opacity": f"0.18 + 0.82*{flash}"})
        layers.append({"type": "shape", "sides": 0, "radius": R + 0.035, "width": 0.006, "fill": 0, "color": col, "x": cx, "y": 0, "opacity": f"0.26 + 0.55*{flash}"})
    return {"background": "#000000", "env": env, "layers": layers, "filters": [{"type": "feedback", "zoom": 1, "decay": 0.955}, bloom(c, 0.4, 0.018, 0.6)]}


@idiom(needs=1, fam="engine", cost=2)
def barber(c):
    """Striped poles, one for each riff: the stripes climb a stripe to the turn, for ever,
    and are never any higher."""
    P = c.riffs[:3]
    layers = [lamp(-3, 5, -6, 1.3), lamp(4, 2, -4, 0.5, c.b), floor(c, 0, "#17171b", 0.6)]
    for i, p in enumerate(P):
        x = (i - (len(P) - 1) / 2) * 2.4
        r = 0.42 - 0.07 * i
        layers.append({"type": "mesh", "shape": "cylinder", "detail": 40, "x": x, "y": 1.75, "z": 0, "scale": 1, "sx": r, "sy": 1.5, "sz": r, **solid(c.col(i), 0.35), "paint_fine": True, "paint_color": "#fff6e6",
                       "paint": f"0.85*step(0.5, fract(vtx.u*{2 + i} + vtx.y*{0.5 + 0.25 * i:g} - {p.turn}))"})
        for y in (0.2, 3.3):
            layers.append(ball(x, y, 0, r * 1.25, 14, sy=0.55, **solid("#b8a468", 0.3, 0.9)))
    look = {"background": c.bg, "layers": layers, "filters": post3d(-3, 5, -6)}
    return shots(c, look, [cam("1.5*sin(time.bar/10)", 1.9, -7.2, look=(0, 1.75, 0), zoom=2.1), cam(-4.2, 0.5, -4.6, look=(0.4, 2.0, 0), zoom=1.5), cam(0, 5.5, -5.2, look=(0, 1.6, 0), zoom=1.7)], P[0], secs=5)


# ───────────── a fifteenth lot: chance and code ─────────────

@idiom(needs=2, fam="game", max_cell=24)
def reels(c):
    """A fruit machine with a reel for each riff: as many faces on it as the riff has
    sixteenths, and it goes a face a sixteenth. The white face is the riff's first; the
    whites stand in a row, and the lamps come on, only when the riffs come round together."""
    P = c.riffs[:3]
    k = len(P)
    h = 1.38
    w = min(2.7, 8.2 / k)
    win = 1.5 * h
    firsts = "*".join(f"(1 - step(1, fract({p.turn})*{p.cell}))" for p in P)
    layers = []
    for i, p in enumerate(P):
        n_ = p.cell
        x = (i - (k - 1) / 2) * w
        u = f"(fract({p.turn})*{n_})"
        # (Faces go by downward, the next one coming from above; each sits still most of its sixteenth and then drops.)
        uu = f"(floor({u}) + smooth(0.55, 1, fract({u})))"
        y = f"((fract((inst.i - {uu})/{n_} + 0.5) - 0.5)*{n_ * h:g})"
        tone = f"step(0.5, inst.i)*(0.3333 + 0.3333*2*fract(inst.i/2))"
        layers.append(box(x, y, 0, w / 2 - 0.17, h / 2 - 0.08, 0.01, count=n_, palette=["#fffaf0", c.col(i), c.dim], pos=tone,
                          emit=f"0.8 + 0.9*(1 - step(0.5, inst.i))*(1 - step({h * 0.6:g}, abs({y})))", light=0, ambient=1, rim=0))
        for sgn in (-1, 1):
            layers.append(box(x + sgn * (w / 2 - 0.06), 0, -0.2, 0.025, win, 0.01, **glow(c.ink, 0.35)))
    for sgn in (-1, 1):
        layers.append(box(0, sgn * (win + 1.4), -0.3, FW + 0.2, 1.4, 0.01, **glow(c.bg, 1)))
        layers.append(box(0, sgn * win, -0.35, k * w / 2, 0.03, 0.01, **glow(c.ink, "0.5 + 2*var.jack")))
        layers.append(box(sgn * (k * w / 2 + 0.22), 0, -0.35, 0.08, 0.05, 0.01, **glow("#ffffff", "0.6 + 2.5*var.jack")))
    layers.append(ball(f"(inst.i - 4)*{k * w / 9:g}", win + 0.45, -0.4, 0.11, 10, count=9, **glow(c.a, f"0.25 + 3*var.jack*(0.5 + 0.5*sin(time.beat*2 + inst.i/3))")))
    return {"background": c.bg, "camera": FLAT, "vars": {"jack": {"follow": firsts, "attack": "0ms", "release": "450ms"}}, "layers": layers,
            "filters": [bloom(c, 0.5, 0.02, 0.7)]}


FACES = {1: [(0, 0)], 2: [(-1, 1), (1, -1)], 3: [(-1, 1), (0, 0), (1, -1)], 4: [(-1, 1), (1, 1), (-1, -1), (1, -1)], 5: [(-1, 1), (1, 1), (0, 0), (-1, -1), (1, -1)],
         6: [(-1, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (1, -1)], 7: [(-1, 1), (1, 1), (-1, 0), (0, 0), (1, 0), (-1, -1), (1, -1)],
         8: [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)], 9: [(-1, 1), (0, 1), (1, 1), (-1, 0), (0, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]}


def _face(count, idx):
    """Where on a die the pip `idx` of a face of `count` goes: two expressions, each -1..1."""
    out = []
    for axis in (0, 1):
        terms = []
        for k, cells in FACES.items():
            inner = [f"{'(0 - 1)' if cell[axis] < 0 else '1'}*(1 - step(0.5, abs({idx} - {j})))" for j, cell in enumerate(cells) if cell[axis]]
            if inner:
                terms.append(f"(1 - step(0.5, abs({count} - {k})))*({' + '.join(inner)})")
        out.append("(" + " + ".join(terms) + ")")
    return out


@idiom(needs=0, fam="game")
def dice(c):
    """Four dice for the four beats of the bar, a row for each of two parts: every note is a
    pip on the die of its beat, set out as on a real die for as many notes as the beat is
    being given, and the dice are thrown again at each bar line."""
    P = _cast(c, 2)
    rows = len(P)
    s = 0.8 if rows == 2 else 1.02
    gap = 2 * s + 0.32
    nb = "floor(fract(time.beat/4)*4)"
    layers = []
    for r, p in enumerate(P):
        y0 = (rows - 1) / 2 * (2 * s + 0.42) - r * (2 * s + 0.42)
        on = f"(1 - step(0.5, abs(inst.i - {nb})))"
        toss = "exp(0 - 9*fract(time.beat/4))"
        layers.append(box(f"(inst.i - 1.5)*{gap:g}", f"{y0:g} + 0.25*{toss}*(1 - 2*fract(inst.i/2))", 0, s, s, 0.02, count=4, round=0.16, rz=f"0.06*{toss}*(1 - 2*fract(inst.i/2))",
                          **glow(("#f3ecd9", "#e9dfc6")[r], f"0.62 + 0.38*{on}")))
        beat = f"floor(({NOTE16})/4 + 0.01)"
        # (How many the beat is being given: one over the wait for the next note; which of them this one is.)
        count = "clamp(floor(1/max(min(note.gap, note.len + 4), 0.1) + 0.5), 1, 9)"
        idx = f"floor(fract(note.beat + 0.002)*{count} + 0.02)"
        fx, fy = _face(count, idx)
        px = f"(({beat} - 1.5)*{gap:g} + {fx}*{s * 0.56:g})"
        py = f"({y0:g} + {fy}*{s * 0.56:g})"
        # Keep previous bar's pips slightly dimmed until overwritten so beats 2-4 never look blank.
        same_bar = f"step(floor(time.beat/4), {NBAR})"
        layers.append(ball(px, py, -0.1, f"{s * 0.17:g}*(1 + 0.7*exp(0 - 7*note.age))", 12, notes={"track": p.name, "past": 4.3}, palette=[c.col(r), "#17151a", "#3a3640"], pos=f"mix(0.85, clamp(note.age*1.2, 0, 0.5), {same_bar})",
                           emit=1, light=0, ambient=1, rim=0, opacity=f"0.42 + 0.58*{same_bar}"))
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.3, 0.014, 0.85)]}


@idiom(needs=1, fam="sign", max_cell=48)
def barcode(c):
    """The riff as a bar code: a bar for each note, as wide as the note is long, laid down
    by a light that reads across once in a turn and gone when the light comes again."""
    P = [p for p in c.riffs if p.cell and p.rate >= 6][:2]
    if not P:
        raise ValueError("too few notes for a code")
    wide = 7.8
    layers = [box(0, 0, 0.3, FW + 0.1, FH + 0.1, 0.01, **glow("#f1ede2", 1))]
    for i, p in enumerate(P):
        m_ = math.ceil(12 / p.cell) if p.cell < 5 else 1      # (a riff of two or three sixteenths is read several turns at a time: two bars are no code)
        n_ = p.cell * m_
        u = wide / n_
        hh = 1.75 if len(P) == 1 else 0.95
        y = (len(P) - 1) * 1.15 - 2.3 * i
        k = f"(floor(fract((note.beat*4 - {p.anchor:g})/{n_} + 0.0005)*{n_}*4 + 0.01)/4)"
        half = f"({u:g}*{p.pitch(0.08, 0.4)})"
        layers.append(box(f"({k} - {n_ / 2:g})*{u:g} + {half}", y, 0, half, hh, 0.01, notes={"track": p.name, "past": n_ / 4 - 0.02}, **glow("#131210", 1)))
        layers.append(box(f"(fract({p.turn}/{m_}) - 0.5)*{wide:g}", y, -0.05, 0.022, hh + 0.14, 0.01, **glow(("#ff2f2f", c.a)[i], 2.2)))
        layers.append(box(0, y - hh - 0.16, 0, wide / 2, 0.012, 0.01, **glow("#131210", 1)))
    return {"background": "#f1ede2", "camera": FLAT, "layers": layers, "filters": [{"type": "grain", "amount": 0.05}]}


@idiom(needs=1, fam="type", cost=2, max_cell=48)
def braille(c):
    """The riff set in braille: six sixteenths to a cell, and a dot stands up for each one
    that sounds, pressed afresh as the riff comes round; a low light goes round the page
    once a turn so the dots throw their shadows."""
    p = c.riffs[0]
    n_ = p.cell
    cells = -(-n_ // 6)
    per_row = cells if cells <= 4 else -(-cells // 2)
    rows = -(-cells // per_row)
    pitch = min(1.05, 7.8 / (per_row * 3.2 - 1.2), 4.5 / (rows * 4.4 - 1.4))

    def place(k):
        cell = f"floor(({k})/6)"
        dot = f"(({k}) - 6*{cell})"
        col = f"floor({dot}/3)"
        row = f"({dot} - 3*{col})"
        cx, cy = f"({cell} - {per_row}*floor({cell}/{per_row}))", f"floor({cell}/{per_row})"
        return (f"(({cx} - {(per_row - 1) / 2:g})*{3.2 * pitch:g} + ({col} - 0.5)*{pitch:g})",
                f"(({(rows - 1) / 2:g} - {cy})*{4.4 * pitch:g} + (1 - {row})*{pitch:g})")
    x0, y0 = place("inst.i")
    x1, y1 = place(f"floor(fract((note.beat*4 - {p.anchor:g})/{n_} + 0.0005)*{n_} + 0.01)")
    th = f"(0.3 + {p.turn}/4)"
    lx, ly = f"7*cos({th})", f"7*sin({th})"
    layers = [lamp(lx, ly, -1.6, 1.5, "#fff1dc", 30), lamp(0, 0, -9, 0.35, "#dfe6ff", 30),
              box(0, 0, 0.12, FW + 0.2, FH + 0.2, 0.1, **solid("#d9d2c2", 0.95)),
              ball(x0, y0, 0.0, pitch * 0.09, 8, count=n_, **solid("#a8a090", 0.9)),
              ball(x1, y1, -0.02, f"{pitch * 0.33:g}*(1 + 0.45*exp(0 - 8*note.age))", 16, notes={"track": p.name, "past": n_ / 4 - 0.02}, **solid("#efe9da", 0.7), sz=0.6)]
    return {"background": "#d9d2c2", "camera": FLAT, "layers": layers, "filters": post3d(lx, ly, -1.6, shadow=0.75, ao=0.35, thr=0.95, glow=0.1)}


# ───────────── a sixteenth lot: two more of what the songs are about ─────────────

def _fib(g):
    """The word the rule makes after g - 1 applications, from one long."""
    w = "L"
    for _ in range(g - 1):
        w = "".join("LS" if ch == "L" else "L" for ch in w)
    return w


@idiom(needs=1, fam="tree", max_cell=64)
def rabbits(c):
    """One rule (a long becomes a long and a short, a short becomes a long) worked out as far
    as the riff is long: each row is the row above with the rule applied once more, and it is
    the same pattern at every size. A light goes across once a turn, and every bar sounds as
    the light comes into it: the top row once a turn, the bottom row a note at a time."""
    lens = {21: 5, 34: 6, 55: 7}
    p = next((p for p in sorted(c.riffs, key=lambda p: -(p.cell or 0)) if p.cell in lens), None)
    if not p:
        raise ValueError("no riff the rule makes")
    G = lens[p.cell]

    def span(ch, k):
        w = ch
        for _ in range(k):
            w = "".join("LS" if x == "L" else "L" for x in w)
        return sum(3 if x == "L" else 2 for x in w)
    wide = 8.3
    unit = wide / p.cell
    rowh = min(0.74, 4.6 / G)
    u = f"(fract({p.turn})*{p.cell})"
    layers = []
    for g in range(1, G + 1):
        y = (G - 1) / 2 * rowh - (g - 1) * rowh
        x0 = 0
        for ch in _fib(g):
            w = span(ch, G - g)
            lit = f"step({x0}, {u})*exp(0 - 1.1*({u} - {x0})/{max(w, 3) / 3:g})"
            layers.append(box((x0 + w / 2 - p.cell / 2) * unit, y, 0, w * unit / 2 - 0.035, rowh / 2 - 0.05, 0.01, **glow(c.a if ch == "L" else c.b, f"0.28 + 1.7*{lit}")))
            x0 += w
    layers.append(box(f"({u} - {p.cell / 2})*{unit:g}", 0, -0.05, 0.014, G * rowh / 2 + 0.1, 0.01, **glow("#ffffff", 1.4)))
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.4, 0.016, 0.7)]}


@idiom(needs=0, fam="wave")
def beats(c):
    """Two notes a hair apart, and what they do together: a row for the note and one for each
    of its overtones, and the swelling goes by once a beat in the first row, twice in the
    second, three times in the third. A part that plays lights the row nearest its own speed."""
    P = _cast(c, 5)
    K = 5
    n_ = 150
    rowh = 4.7 / K
    wide = 8.6
    layers = []
    for k in range(1, K + 1):
        y = (K - 1) / 2 * rowh - (k - 1) * rowh
        x = f"((inst.i + 0.5)/{n_} - 0.5)"
        # (Four beats across the frame; the swelling goes left a beat a beat.)
        env = f"abs(cos(0.5*{k}*({x}*4 + time.beat)))"
        fine = f"(0.55 + 0.45*sin(inst.i*0.31))"
        loud = f"(0.75 + 1.3*{P[(k - 1) % len(P)].hit})" if P else "1"
        layers.append(box(f"{x}*{wide:g}", y, 0, wide / n_ * 0.33, f"{rowh * 0.46:g}*{env}*{fine} + 0.006", 0.01, count=n_, opacity="step(0.5, inst.i)", **glow(c.col(k - 1), f"(0.35 + 0.9*{env})*{loud}")))
    layers.append(box(0, 0, -0.05, 0.008, 2.45, 0.01, **glow(c.ink, 0.5)))
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.45, 0.018, 0.6)]}


@idiom(needs=0, fam="count")
def total(c):
    """A riff added up: its first place, its first two, its first three. A row for each
    statement, one place longer than the last, so every place of the riff has a column of
    its own, and each cell is lit as it is played. The cells that fall on a bar line carry a
    white mark: they wander, and one stands at the end of a row only when the riff is whole.
    The frame holds as much of the triangle as has been played, and draws back as it grows."""
    A = getattr(c, "adding", None)
    if not A:
        raise ValueError("nothing is being added up here")
    kind, s0, k0, L, keys = A
    W_, H_ = 8.7, 4.85
    w0, h0 = W_ / L, H_ / L
    now = "(time.beat*4)"
    pitched = [k for k in keys if k is not None] or [0]
    lo, hi = min(pitched), max(pitched)
    end = s0 + L * (L + 1) // 2
    done = f"step({end}, {now})*exp(0 - 0.35*max({now} - {end}, 0))"
    rows = f"((sqrt(8*max({now} - {s0}, 0) + 1) - 1)/2)"
    z = "var.z"
    layers = []
    for j in range(L):
        first = j + 1 if kind == "head" else L - j
        k = f"({first} + inst.i)"
        idx = f"{j}" if kind == "head" else f"({j - L} + {k})"
        when = f"({s0} + {k}*({k} - 1)/2 + {idx})"
        x = f"({-W_ / 2:g} + {(j + 0.5) * w0:g}*{z})" if kind == "head" else f"({W_ / 2:g} - {(L - j - 0.5) * w0:g}*{z})"
        y = f"({H_ / 2:g} - ({k} - 0.5)*{h0:g}*{z})"
        lit = f"step({when}, {now})"
        fresh = f"exp(0 - 0.5*max({now} - {when}, 0))"
        played = f"(0.3 + 0.7*step({k0 - 0.5}, {k}))"
        sx, sy = f"{w0 * 0.42:g}*{z}", f"{h0 * 0.36:g}*{z}"
        if keys[j] is None:
            layers.append(box(x, y, 0, sx, sy, 0.01, count=L - first + 1, **glow(c.dim, f"0.12 + {lit}*(0.22 + 0.6*{fresh}) + 0.6*{done}")))
        else:
            layers.append(box(x, y, 0, sx, sy, 0.01, count=L - first + 1, palette=[c.a, c.b, c.c, c.ink], pos=0.999 * (keys[j] - lo) / max(hi - lo + 1, 1),
                              emit=f"0.09 + {played}*{lit}*(0.8 + 2.4*{fresh}) + 1.2*{done}", light=0, ambient=1, rim=0))
        bar = f"(1 - step(0.5, fract(({when})/16 + 0.001)*16))"
        layers.append(ball(x, f"{y} + {h0 * 0.36:g}*{z}", -0.05, f"{min(h0 * 0.3, 0.06):g}*{z}*{bar}", 8, count=L - first + 1, **glow("#ffffff", f"0.55 + 1.6*{lit}")))
    return {"background": c.bg, "camera": FLAT, "vars": {"z": {"follow": f"clamp({L}/({rows} + 3), 1, 3.2)", "attack": "0ms", "release": "0ms"}}, "layers": layers,
            "filters": [bloom(c, 0.4, 0.014, 0.75)]}


@idiom(needs=0, fam="engine")
def zipper(c):
    """A zip fastener being closed: the teeth of one side are one part's notes and the teeth
    of the other side another's, each as wide as the pulse they share. Where each plays only
    where the other rests the teeth mesh and the zip closes without a gap."""
    fit = getattr(c, "fit", None)
    if not fit:
        raise ValueError("no two parts here fit into one another")
    P = list(fit[:2])
    step = fit[2]                                  # beats to a tooth
    u = min(0.42 / step, 1.9)                      # frame units a beat
    tw = step * u
    xs = 1.6                                       # where the slider is
    layers = []
    for side, p in ((1, P[0]), (-1, P[1])):
        x = f"({xs} - note.age*{u:g} + {tw / 2:g})"
        apart = f"smooth(0, 1, (0 - note.age)*{u:g}/2.6)"
        y = f"({side}*(0.34 + 1.25*{apart}))"
        col = c.col(0 if side > 0 else 1)
        layers.append(box(x, y, 0, tw * 0.43, 0.52, 0.02, notes={"track": p.name, "past": 9.5 / u, "ahead": 3.6 / u}, rz=f"{side}*0.09*{apart}", **glow(col, f"0.75 + 1.8*exp(0 - 3*abs(note.age))")))
        # (The tape each side's teeth are sewn to.)
        xi = f"(inst.i/59*9.4 - 4.7)"
        ap = f"smooth(0, 1, ({xi} - {xs})/2.6)"
        layers.append(box(xi, f"{side}*(1.0 + 1.25*{ap})", 0.05, 0.085, 0.16, 0.01, count=60, rz=f"{side}*0.09*{ap}", **glow(c.dim, 0.9)))
    layers.append(box(xs + 0.12, 0, -0.1, 0.2, 0.62, 0.04, round=0.12, **glow(c.ink, f"0.8 + 0.9*max({P[0].hit}, {P[1].hit})")))
    layers.append(box(xs - 0.25, 0, -0.12, 0.16, 0.1, 0.02, round=0.06, **glow(c.ink, 0.7)))
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.4, 0.016, 0.7)]}


@idiom(needs=0, fam="count")
def squares(c):
    """A walk of numbers, each of which lasts as many sixteenths as it is: every number is a
    square, as wide as it lasts and as high, standing on a line that goes by at one speed.
    The frame fits the number being played, so it draws back when a number is trebled and
    comes in as the numbers are halved, down to one. A number that is three times the last
    and one more shows its three parts and, in white, the one."""
    W = getattr(c, "walk", None)
    if not W:
        raise ValueError("no part here walks from number to number")
    steps, part = W
    now = "(time.beat*4)"
    base, x0, cap = -2.05, -1.7, 0.6
    def fit(k):
        m = steps[k][1]
        nx = steps[k + 1][1] if k + 1 < len(steps) else m
        return min(cap, 3.5 / max(m, 0.8 * nx))
    # How big a sixteenth is drawn: a step up or down at each new number, taken smoothly.
    first = next((k for k in range(len(steps)) if steps[k][0] + steps[k][1] > c.a16), 0)
    target = f"{fit(first):.4g}"
    for k in range(first + 1, len(steps)):
        d = fit(k) - fit(k - 1)
        if abs(d) > 1e-4:
            target += f" + {n(round(d, 4))}*step({steps[k][0] - 2}, {now})"      # (a little before, so it is seen coming)
    u = "var.u"
    layers = []
    hit = f"track.{part}.hit"
    for k, (s0, m, added) in enumerate(steps):
        xl = f"({x0} + ({s0} - {now})*{u})"
        side = f"({m}*{u})"
        vis = f"step({xl}, 4.8)*step((0 - 4.8), {xl} + {side})"
        col = "#ffffff" if m == 1 else (c.a if m % 2 == 0 else c.b)
        cur = f"step({s0}, {now})*step({now}, {s0 + m})"
        done = f"step({s0 + m}, {now})"
        # The square: dim until it is played, and a little lighter once it has been.
        layers.append(box(f"{xl} + {side}/2", f"{base} + {side}/2", 0.02, f"max({side}/2 - 0.014, 0.004)*{vis}", f"max({side}/2 - 0.014, 0.004)", 0.01, **glow(col, f"0.24 + 0.14*{done}")))
        # As much of it as has been played.
        w = f"(clamp({now} - {s0}, 0, {m})*{u})"
        layers.append(box(f"{xl} + {w}/2", f"{base} + {side}/2", 0, f"max({w}/2 - 0.014, 0)*{vis}", f"max({side}/2 - 0.014, 0.004)", 0.01, **glow(col, f"0.42 + 0.65*{cur} + 1.5*{cur}*{hit} + 0.3*{done}*exp(0 - 0.08*({now} - {s0 + m}))")))
        if added and m > 4:
            # Three times the last number, and one: the one in white, and the three marked off.
            prev = (m - 1) // 3
            layers.append(box(f"{xl} + {u}/2", f"{base} + {side}/2", -0.02, f"{u}/2*{vis}", f"{side}/2", 0.01, **glow("#ffffff", f"0.45 + 0.9*{cur}")))
            for j in (1, 2):
                layers.append(box(f"{xl} + {1 + j * prev}*{u}", f"{base} + {side}/2", -0.02, f"0.012*{vis}", f"{side}/2", 0.01, **glow(c.bg, 1)))
    # The line they stand on, ruled in sixteenths (where they are big enough to see) and in bars.
    layers.append(box(0, base - 0.03, 0, 4.8, 0.012, 0.01, **glow(c.ink, 0.8)))
    layers.append(box(f"{x0} + (inst.i - 24 - fract({now}))*{u}", base - 0.1, 0, 0.008, f"0.06*smooth(0.1, 0.3, {u})", 0.01, count=72, **glow(c.ink, 0.7)))
    layers.append(box(f"{x0} + ((inst.i - 12)*16 - fract({now}/16)*16)*{u}", base - 0.16, 0, 0.014, 0.12, 0.01, count=40, **glow(c.ink, 0.9)))
    # Now.
    layers.append(box(x0, 0.25, -0.04, 0.01, 2.4, 0.01, **glow("#ffffff", f"0.5 + 1.2*{hit}")))
    return {"background": c.bg, "camera": FLAT, "vars": {"u": {"follow": target, "attack": "260ms", "release": "260ms"}}, "layers": layers,
            "filters": [bloom(c, 0.4, 0.014, 0.75)]}


@idiom(needs=0, fam="trace")
def ringing(c):
    """Rows as they are rung: the same few notes, each time in a new order, no note moving
    more than one place. Each row is written across as it is played, a dot a note, and every
    note has a line that runs down through its places from row to row; the highest note's
    line is white. A row in which the notes stand in order of pitch is ruled across."""
    R = getattr(c, "rows", None)
    if not R:
        raise ValueError("nothing is being rung in changes here")
    rows, part = R                                  # [(sixteenth, length, ((sixteenth, key), ...))]
    bells = sorted({k for _, _, row in rows for _, k in row}, reverse=True)
    N = len(bells)
    now = "(time.beat*4)"
    dx, gap, ynow = min(1.4, 8.2 / N), 0.3, -1.95
    xs = lambda j: (j - (N - 1) / 2) * dx                                     # noqa: E731
    tint = lambda b: "#ffffff" if b == bells[0] else (c.dim if b == bells[-1] else (c.a, c.b, c.c, c.ink)[bells.index(b) % 4])   # noqa: E731
    layers = []
    for k, (s0, L, row) in enumerate(rows):
        y = f"({ynow} + ({now} - {s0})*{gap / L:g})"
        order = [key for _, key in row]
        for j, (on, key) in enumerate(row):
            fresh = f"step({on}, {now})*exp(0 - 0.7*({now} - {on}))"
            layers.append(ball(xs(j), y, -0.05, f"{0.085 if key == bells[0] else 0.062}*step({on}, {now})*(1 + 0.8*{fresh})", 6, **glow(tint(key), f"0.5 + 2.2*{fresh}")))
            if k + 1 < len(rows) and rows[k + 1][0] == s0 + L and key in [q for _, q in rows[k + 1][2]]:
                s1, L1, nxt = rows[k + 1]
                j1 = [q for _, q in nxt].index(key)
                y1 = f"({ynow} + ({now} - {s1})*{gap / L1:g})"
                # The line to its place in the next row is drawn as that row is rung.
                g = f"clamp(({now} - {s1})/{L1}*1.6, 0, 1)"
                layers.append({"type": "beam", "from": [xs(j), y, 0], "to": [f"{xs(j):g} + {n(xs(j1) - xs(j))}*{g}", f"{y} + ({y1} - {y})*{g}", 0],
                               "width": 0.05 if key == bells[0] else 0.02, "samples": 2, "glow": f"(1.3 if 0 else 1)*step({s1}, {now})*{1.3 if key == bells[0] else 0.75}".replace("(1.3 if 0 else 1)*", ""), "fade": 0, "color": tint(key)})
        # The line to its place in the next row is drawn as that row is rung.
        if order == bells and k:
            layers.append(box(0, y, 0.03, xs(N - 1) + 0.45, 0.008, 0.01, **glow("#ffffff", f"0.95*step({s0 + L}, {now})")))
    # Extent gauge along the left margin: shows the row length (8 sixteenths in extent 1,
    # 10 in extent 2) as stacked notches with the live position inside the current row.
    L0 = rows[0][1]
    ph_row = f"fract(({now} - {rows[0][0]})/{L0})"
    here_slot = f"floor({ph_row}*{L0})"
    for j in range(L0):
        ym = 2.0 - j * (4.0 / max(L0 - 1, 1))
        layers.append(box(-4.22, ym, 0, 0.14 if j in (0, L0 - 1) else 0.09, 0.055, 0.01,
                          **glow(c.a if L0 <= 8 else c.b, f"0.25 + 2.2*(1 - step(0.5, abs({j} - {here_slot})))")))
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.4, 0.014, 0.7)]}


@idiom(needs=0, fam="wave")
def rolls(c):
    """A roll too fast to count, slowed until it can be (or wound up until it cannot): a ring
    for each drum of the roll, and every stroke a dot on its ring at its place in the beat.
    Rolled, a ring is whole: a note. Slowing, its dots draw apart into arms that turn. Slow
    enough to count, a stroke on every beat stands still, and strokes that cross the beat
    step round it."""
    R = getattr(c, "roll", None)
    if not R:
        raise ValueError("nothing is being rolled here")
    part, lo, hi = R
    span = max(hi - lo, 1)
    # A stroke is born on its drum's ring and drifts outward for four beats: a steady pulse
    # leaves a line of dots, a roll a whole band, a slowing roll arms that open out.
    rad = f"(0.17 + 0.5*(note.midi - {lo})/{span} + 0.25*clamp(note.age/4, 0, 1))"
    ang = "fract(note.beat + 0.0005)"
    fresh = "exp(0 - 5*max(note.age, 0))"
    size = "clamp(0.011 + 0.035*min(note.gap, 1), 0.011, 0.046)"
    layers = [{"type": "shape", "repeat": 4, "sides": 0, "radius": "0.17 + 0.25*inst.i", "width": 0.0025, "fill": 0, "color": c.dim, "opacity": 0.6, "blend": "normal", "x": 0, "y": 0},
              # One beat round: a mark at the top where the beat falls.
              {"type": "shape", "sides": 4, "rotate": 0.125, "radius": 0.022, "width": 0, "fill": 1, "color": "#ffffff", "x": 0, "y": 0.96, "opacity": "0.5 + 0.5*pow(1 - time.phase, 4)"},
              {"type": "shape", "notes": {"track": part, "past": 4, "ahead": 0}, "count": 4000, "sides": 1, "radius": f"{size}*(1 + 1.1*{fresh})", "width": 0, "fill": 1,
               "palette": [c.a, c.b, c.c], "pos": f"0.999*(note.midi - {lo})/{span}", "x": f"{rad}*sin({ang})", "y": f"{rad}*cos({ang})",
               "opacity": f"clamp(0.55 + 0.45*{fresh}, 0, 1)*(1 - 0.75*clamp(note.age/4, 0, 1))"},
              {"type": "shape", "notes": {"track": part, "past": 0.5, "ahead": 0}, "count": 600, "sides": 1, "radius": f"{size}*2*{fresh}", "width": 0, "fill": 1, "color": "#ffffff",
               "x": f"{rad}*sin({ang})", "y": f"{rad}*cos({ang})", "opacity": f"0.8*{fresh}"}]
    return {"background": c.bg, "layers": layers, "filters": [bloom(c, 0.5, 0.012, 0.6)]}


@idiom(needs=0, fam="count")
def ledger(c):
    """A phrase whose first half borrows time from its second and pays it back. A row for each
    time the phrase is played, as long as the phrase: its notes are blocks as long as they
    last, the first half's in one colour and the second's in another, and under them each
    half is ruled off as long as it was given. A white line stands down the middle, where the
    halves would meet if neither owed the other anything; what is owed is the lit block
    between that line and where the second half begins."""
    R = getattr(c, "owing", None)
    if not R:
        raise ValueError("nothing is owed here")
    part, rows, L = R
    now = "(time.beat*4)"
    gap = max(0.8, min(1.5, 4.6 / max(len(rows), 1)))          # (few rows: taller ones)
    u, ynow, k = 8.5 / L, -2.05, gap / 0.8
    lo = min(k for _, _, ns in rows for _, _, k, _ in ns)
    hi = max(k for _, _, ns in rows for _, _, k, _ in ns)
    layers = [box(0, 0, 0.05, 0.008, 2.6, 0.01, **glow("#ffffff", 0.75))]
    for i, (s0, B, ns) in enumerate(rows):
        # A row rises as it is played, and again as each later row is: so the ledger stands
        # still while the phrase is not being played, and what was owed before stays written.
        rise = " + ".join(f"clamp(({now} - {r[0]})/{L}, 0, 1)" for r in rows[i:])
        y = f"({ynow} + ({rise})*{gap:g})"
        seen = f"step({s0}, {now})"
        for on, ln, key, second in ns:
            w = max(ln, 0.35) * u / 2
            fresh = f"step({s0 + on:g}, {now})*exp(0 - 0.5*({now} - {s0 + on:g}))"
            layers.append(box((on - L / 2) * u + w, f"{y} + {k * (0.22 + 0.4 * (key - lo) / max(hi - lo, 1)):g}", 0, w - 0.012, 0.045 * k, 0.01,
                              **glow(c.b if second else c.a, f"step({s0 + on:g}, {now})*(0.8 + 1.6*{fresh})")))
        # Each half ruled off as long as it was given, drawn as the phrase goes by.
        for x0, x1, col in ((0, B, c.a), (B, L, c.b)):
            g = f"clamp(({now} - {s0 + x0:g})/{max(x1 - x0, 1):g}, 0, 1)"
            layers.append(box(f"{(x0 - L / 2) * u:g} + {(x1 - x0) * u / 2:g}*{g}", f"{y} + {0.08 * k:g}", 0.01, f"{(x1 - x0) * u / 2 - 0.01:g}*{g}", 0.03 * k, 0.01, **glow(col, f"0.55*{seen}")))
        if abs(B - L / 2) >= 0.4:
            # What is owed: between the middle and where the second half begins.
            x0, x1 = sorted((L / 2, B))
            layers.append(box(((x0 + x1) / 2 - L / 2) * u, f"{y} + {0.08 * k:g}", -0.01, (x1 - x0) * u / 2, 0.075 * k, 0.01,
                              **glow("#ffffff", f"step({s0 + x0:g}, {now})*(0.8 + 1.4*exp(0 - 0.25*max({now} - {s0 + x0:g}, 0)))")))
    # Where the phrase is now.
    cur = f"(fract(({now} - {rows[-1][0]})/{L}) - 0.5)*{L * u:g}"
    layers.append(box(cur, ynow + 0.4 * k, -0.03, 0.014, 0.4 * k, 0.01, **glow(c.ink, 1.3)))
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.4, 0.014, 0.7)]}


@idiom(needs=0, fam="count")
def sizes(c):
    """One rule played at several sizes at once. Each part that plays only a long and a short
    (three sixteenths and two; five and three; eight and five) is a course of bricks, a brick
    for each note, as long as the time to the next: long bricks one colour, short ones
    another. The courses lie one over the other on one scale of time, the biggest size at the
    top, so it can be seen that a long of one course is a long and a short of the course
    below, and a short is its long: the same wall at every size. A brick lights as its note
    is struck and stays lit; a line shows where the music is. Where only one size is played,
    the sizes the rule implies stand over it, dimly, and fill in as it goes. The frame holds
    the stretch of the wall the scene plays, and a bar to either side."""
    R = getattr(c, "sizes", None)
    if not R:
        raise ValueError("nothing is played at several sizes here")
    rows = R[2]
    # (the stretch shown: the scene and a bar before and after, four bars at least, within the passage)
    a, b = max(R[0], c.a16 - 16), min(R[1], c.b16 + 16)
    if b - a < 64:
        a = max(R[0], min(a, b - 64))
        b = min(R[1], max(b, a + 64))
    now = "(time.beat*4)"
    courses = [(L, S, [(on, gap) for on, gap, _ in ns], True) for _, L, S, ns in rows]
    while len(courses) < 3:
        # The next size up: a long and the short after it are its long; a long alone is its short.
        L, S, ns, _ = courses[0]
        up, i = [], 0
        while i < len(ns):
            on, gap = ns[i]
            if gap == L and i + 1 < len(ns) and ns[i + 1][1] == S:
                up.append((on, L + S))
                i += 2
            else:
                up.append((on, gap))
                i += 1
        if len(up) < 4:
            break
        courses.insert(0, (L + S, L, up, False))
    wide = 7.9
    u = wide / max(b - a, 1)
    n_ = len(courses)
    hh = min(1.25, 4.4 / n_ - 0.14)
    layers = []
    for k, (L, S, ns, played) in enumerate(courses):
        y = ((n_ - 1) / 2 - k) * (hh + 0.14)
        for on, gap in ns:
            x0, x1 = max(on, a), min(on + gap, b)
            if x1 - x0 < 0.25:
                continue            # (not in the stretch shown)
            half = (x1 - x0) * u / 2
            col = c.a if gap == L else c.b if gap == S else c.dim
            struck = f"step({on:g}, {now})"
            emit = (f"0.16 + {struck}*(0.5 + 1.7*exp(0 - 0.45*max({now} - {on:g}, 0)))" if played
                    else f"0.09 + 0.24*{struck}")
            layers.append(box((x0 - a) * u - wide / 2 + half, y, 0, max(half - 0.02, 0.01), hh / 2, 0.01, **glow(col, emit)))
    cur = f"clamp(({now} - {a:g})/{max(b - a, 1):g}, 0, 1)*{wide:g} - {wide / 2:g}"
    layers.append(box(cur, 0, -0.03, 0.012, n_ * (hh + 0.14) / 2 + 0.1, 0.01, **glow(c.ink, 1.3)))
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.4, 0.014, 0.7)]}


@idiom(needs=0, fam="count")
def pinion(c):
    """A riff one place shorter than the bar (or one longer). The bar is a ring of teeth,
    one for every place in it, and the point where the music is goes round it once a bar.
    The riff is a wheel with a tooth for every place in the riff, rolling inside the ring
    (a hoop rolling round it, if the riff is the longer): at every place one tooth of each
    meets, so the wheel falls a tooth behind every bar. A note is a tooth lit where it
    was struck, and it stays lit for one turn of the wheel: the riff is seen going round,
    and what answers it lights the teeth between. One tooth is marked and draws its path:
    it is back where it was after as many bars as the riff has places. (Where a band has
    begun to count faster, its bar is a wheel shorter round than the ring but with as many
    teeth: sixteen on a wheel fifteen round.)"""
    R = getattr(c, "gear", None)
    if not R:
        raise ValueError("no riff is a place off the bar here")
    sub, g, wheels = R
    big = max(w[0] for w in wheels)
    rr = 3.05 if big < g else 2.8
    tau = f"(time.beat*{sub})"
    phi = f"({tau}/{g})"
    beat = f"(1 - step(0.5, fract(inst.i/{sub})*{sub}))"
    layers = [ball(f"{rr:g}*sin(inst.i/{g})", f"{rr:g}*cos(inst.i/{g})", 0, f"0.055 + 0.05*{beat}", 6, count=g, **glow(c.ink, f"0.6 + 0.8*{beat}")),
              ball(f"{rr:g}*sin(inst.i/240)", f"{rr:g}*cos(inst.i/240)", 0, 0.016, 4, count=240, **glow(c.dim, 1.1))]
    env = {}
    for w, (P, q0, parts, *more) in enumerate(wheels[:3]):
        teeth = more[0] if more else P                     # (a wheel fifteen places round may carry sixteen teeth: a band that counts faster)
        rp = rr * P / g
        d = rr - rp
        psi = f"({tau}/{g} - ({tau} - {q0})/{P})"
        hx, hy = f"({d:g}*sin({phi}))", f"({d:g}*cos({phi}))"
        at = lambda ang, r=rp: (f"{hx} + {r:g}*sin({ang})", f"{hy} + {r:g}*cos({ang})")      # noqa: E731
        x, y = at(f"(inst.i/240 + {psi})")
        layers.append(ball(x, y, 0, 0.018, 4, count=240, **glow(c.col(2 * w), 0.9)))
        x, y = at(f"(inst.i/{teeth} + {psi})")
        layers.append(ball(x, y, 0, 0.075, 6, count=teeth, **glow(c.dim, 1.3)))
        # the marked tooth's path over the whole cycle, and the tooth on it
        m = g * P
        ti = f"({q0} + inst.i*{m / 600:g})"
        layers.append(ball(f"{d:g}*sin({ti}/{g}) + {rp * 0.8:g}*sin({ti}/{g} - ({ti} - {q0})/{P})", f"{d:g}*cos({ti}/{g}) + {rp * 0.8:g}*cos({ti}/{g} - ({ti} - {q0})/{P})", 0.02, 0.013, 4, count=600,
                           **glow(c.col(2 * w), 0.8)))
        x, y = at(psi)
        layers.append({"type": "beam", "from": [hx, hy, 0], "to": [x, y, 0], "width": 0.02, "samples": 8, "color": c.ink, "glow": 0.7})
        x, y = at(psi, rp * 0.8)
        layers.append(ball(x, y, -0.02, 0.1, 8, **glow(c.ink, 1.4)))
        layers.append(ball(hx, hy, 0, 0.09, 8, **glow(c.col(2 * w), 1.0)))
        for j, nm in enumerate(parts[:2]):
            col = c.col(2 * w + j)
            x, y = at(f"((note.beat*{sub} - {q0})/{P} + {psi})", rp * (1 - 0.07 * j))
            layers.append(ball(x, y, -0.04, f"{0.21 - 0.04 * j:g}*(1 + 0.5*exp(0 - 5*max(note.age, 0)))", 10, notes={"track": nm, "past": P / sub - 0.02, "ahead": 0}, count=2 * P,
                               **glow(col, "0.7 + 2*exp(0 - 4*max(note.age, 0))")))
            env[f"g{w}{j}"] = {"on": f"track.{nm}", "attack": "0ms", "decay": "140ms"}
    hit = " + ".join(f"env.{k}" for k in env)
    layers.append(ball(f"{rr:g}*sin({phi})", f"{rr:g}*cos({phi})", -0.06, f"0.1 + 0.14*min({hit}, 1)", 8, **glow("#ffffff", f"0.8 + 2.2*min({hit}, 1)")))
    # (The ring lies back: seen from below its near edge, it fills the width of the frame.)
    return {"background": c.bg, "env": env, "camera": {"x": 0, "y": -6.0, "z": -6.8, "look_at": [0, -0.42, 0], "zoom": 2.2}, "layers": layers, "filters": [bloom(c, 0.45, 0.016, 0.6)]}


@idiom(needs=0, fam="count")
def cobweb(c):
    """A tune made by a rule, in which every note's pitch decides the next one's. Across
    is the pitch of a note, up is the pitch of the note after it; a slanting line marks
    where the two are the same. Every note is a point, so the points lie on the rule
    itself, an arch, and draw it. From each note a line goes up to its point and across to
    the slant, where the next note starts: while the tune only goes to and fro the line
    goes round one box, round two when it takes four notes to come back, and when it
    never comes back it wanders all over the arch."""
    R = getattr(c, "rule", None)
    if not R:
        raise ValueError("no tune is made by a rule here")
    nm, lo, hi, step = R
    lo, hi = lo - 1.5, hi + 1.5
    w, h = 3.9, 2.2
    gap = step / 4                                         # (beats between notes)
    xa = f"({n(-w)} + {2 * w / (hi - lo):g}*(note.midi - {lo:g}))"
    ya = f"({n(-h)} + {2 * h / (hi - lo):g}*(note.midi - {lo:g}))"
    nx = "(note.next_key*84 + 24)"
    xb = f"({n(-w)} + {2 * w / (hi - lo):g}*({nx} - {lo:g}))"
    yb = f"({n(-h)} + {2 * h / (hi - lo):g}*({nx} - {lo:g}))"
    tr = {"track": nm, "past": 96, "ahead": 0}
    web = {"track": nm, "past": 10 * gap, "ahead": 0}
    done = f"step({gap:g}, note.age)"
    fade = f"exp(0 - {0.22 / gap:g}*max(note.age - {gap:g}, 0))"
    layers = [box(0, -h - 0.06, 0, w + 0.1, 0.014, 0.014, **glow(c.dim, 1.4)), box(-w - 0.06, 0, 0, 0.014, h + 0.1, 0.014, **glow(c.dim, 1.4)),
              ball(f"{n(-w)} + inst.i*{2 * w / 71:g}", f"{n(-h)} + inst.i*{2 * h / 71:g}", 0.02, 0.024, 4, count=72, **glow(c.dim, 1.6)),
              # every pair there has been: the rule, drawn by the tune
              ball(xa, yb, 0, f"0.10*{done}", 6, notes=tr, count=96, **glow(c.b, f"(0.95 + 1.1*exp(0 - 0.05*note.age))*{done}")),
              # the web: up from the slant to the point, across to the slant again
              {"type": "beam", "notes": web, "count": 12, "from": [xa, ya, 0], "to": [xa, yb, 0], "width": 0.048, "samples": 6, "color": c.a,
               "reach": f"clamp(note.age*{2 / gap:g}, 0, 1)", "glow": f"(0.65 + 1.4*(1 - {done}))*{fade}"},
              {"type": "beam", "notes": web, "count": 12, "from": [xa, yb, 0], "to": [xb, yb, 0], "width": 0.048, "samples": 6, "color": c.a,
               "reach": f"clamp(note.age*{2 / gap:g} - 1, 0, 1)", "glow": f"(0.65 + 1.4*(1 - {done}))*{fade}*step({gap / 2:g}, note.age)"},
              # the note that sounds, on the slant, and where it stands along the bottom
              ball(xa, ya, -0.03, f"0.18*(1 - {done})*(1 + 0.6*exp(0 - 4*note.age))", 10, notes={"track": nm, "past": gap, "ahead": 0}, count=2, **glow(c.ink, f"1.7*(1 - {done})")),
              box(xa, -h - 0.16, 0, 0.024, 0.1, 0.02, notes={"track": nm, "past": gap, "ahead": 0}, count=2, **glow(c.ink, f"1.5*(1 - {done})"))]
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.45, 0.016, 0.6)]}


def _log2(x):
    """log2 of an expression (there is no log: the limit of (x^e - 1)/e does for one)."""
    return f"((pow({x}, 0.002) - 1)*721.35)"


@idiom(needs=0, fam="count")
def spire(c):
    """Voices an octave apart, all on one note, and the note climbing (or falling) for ever.
    A winding stair, a turn to the octave, seen from the side and from above. From the
    side every note is a tread at the height of its pitch: the voices stand over one
    another, a turn apart, and all go up together; the lowest comes in dim as the highest
    goes out. From above the same treads lie on one spoke, the higher the further out, and
    the spoke goes round like a hand: it is never any higher."""
    R = getattr(c, "climb", None)
    if not R:
        raise ValueError("no voices climb an octave apart here")
    names, lo, hi = R
    names = names[:5]
    span = max(hi - lo, 12)
    ex, er, px, pr = -2.35, 1.85, 2.3, 2.05
    th = "(note.midi/12)"
    y = f"((note.midi - {(lo + hi) / 2:g})*{4.4 / span:g})"
    out = f"({pr:g}*(0.2 + 0.8*clamp((note.midi - {lo:g})/{span:g}, 0, 1)))"
    lit = "(0.45 + 0.7*exp(0 - 0.3*max(note.age, 0)))*(0.7 + 1.7*note.on)*(0.5 + 0.8*note.vel)"
    nn = 6 * span + 1
    mi = f"({lo:g} + inst.i/6)"
    layers = [box(ex, 0, 0, 0.02, 2.3, 0.02, **glow(c.dim, 1.2)),
              # the stair's rail: a thread round the column, dimmer where it goes behind
              ball(f"{n(ex)} + {er:g}*sin({mi}/12)", f"({mi} - {(lo + hi) / 2:g})*{4.4 / span:g}", f"0 - {er:g}*cos({mi}/12)", 0.03, 4, count=nn,
                   **glow(c.dim, f"0.8 + 1.2*(0.5 + 0.5*cos({mi}/12))")),
              # the dial: twelve places round, one for each note there is
              ball(f"{px:g} + {pr * 1.07:g}*sin(inst.i/12)", f"{pr * 1.07:g}*cos(inst.i/12)", 0, 0.062, 6, count=12, **glow(c.dim, 1.6)),
              ball(f"{px:g} + {pr:g}*sin(inst.i/120)", f"{pr:g}*cos(inst.i/120)", 0, 0.02, 4, count=120, **glow(c.dim, 1.1))]
    for i, nm in enumerate(names):
        col = c.col(i)
        tr = {"track": nm, "past": 12, "ahead": 0}
        # from the side: a tread from the column out to the rail, and a bead on its end
        layers.append(box(f"{n(ex)} + {er / 2:g}*sin({th})", y, f"0 - {er / 2:g}*cos({th})", f"0.02 + {er / 2:g}*abs(sin({th}))", 0.042, 0.02, notes=tr, count=40,
                          **glow(col, f"0.7*{lit}")))
        layers.append(ball(f"{n(ex)} + {er:g}*sin({th})", y, f"0 - {er:g}*cos({th})", "0.115*(1 + 0.6*note.on)", 8, notes=tr, count=40, **glow(col, lit)))
        # from above: the same notes on one spoke
        layers.append(ball(f"{px:g} + {out}*sin({th})", f"{out}*cos({th})", 0, "0.115*(1 + 0.6*note.on)", 8, notes=tr, count=40, **glow(col, lit)))
    k = f"((track.{names[0]}.key*84 + 24)/12)"
    layers.append({"type": "beam", "from": [px, 0, 0], "to": [f"{px:g} + {pr:g}*sin({k})", f"{pr:g}*cos({k})", 0], "width": 0.034, "samples": 8, "color": c.ink,
                   "glow": f"0.8 + 1.1*track.{names[0]}.level"})
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.45, 0.016, 0.6)]}


@idiom(needs=0, fam="count")
def quicken(c):
    """Parts an octave of speed apart, all gaining for ever. Every stroke is a tick, set
    down where it fell (the newest at the right) and as high as its part is quick: each
    part is a row of ticks closing up and bending upward, twice as close as the row below.
    The top row thins out as it goes and a new one comes in underneath, wide apart. At the
    right the same strokes go round a dial, a turn to the stroke, the quicker further out:
    the hands lap one another two for one, and all pass the top together."""
    R = getattr(c, "quick", None)
    if not R:
        raise ValueError("no parts gain an octave of speed apart here")
    names, g0, g1 = R
    names = names[:6]
    l0, l1 = math.log2(g1 / 4), math.log2(g0 / 4)          # (slowest and quickest gaps, in beats)
    u = f"clamp(({l0:g} - {_log2('clamp(note.gap, 0.04, 4)')})/{l0 - l1:g}, 0 - 0.08, 1.08)"
    nx, px, pr = 1.2, 3.05, 1.4
    lit = "(0.45 + 0.55*exp(0 - 0.35*max(note.age, 0)))*(0.6 + 1.6*note.on)*(0.45 + 0.8*note.vel)"
    layers = [box(nx, 0, 0, 0.01, 2.35, 0.01, **glow(c.dim, 1.0)),
              ball(f"{px:g} + {pr:g}*sin(inst.i/96)", f"{pr:g}*cos(inst.i/96)", 0, 0.014, 4, count=96, **glow(c.dim, 0.8)),
              box(px, pr + 0.13, 0, 0.014, 0.1, 0.014, **glow(c.ink, 1.2))]
    for i, nm in enumerate(names):
        col = c.col(i)
        layers.append(box(f"{nx:g} - note.age*{5.7 / 6:g}", f"0 - 1.7 + 3.4*{u}", 0, 0.026, "0.11 + 0.22*note.vel", 0.02, notes={"track": nm, "past": 6, "ahead": 0}, count=96,
                          **glow(col, lit)))
        on = "step(0, note.age)*(1 - step(note.gap, note.age))"
        rr = f"({pr:g}*(0.22 + 0.78*{u}))"
        ang = "(note.age/max(note.gap, 0.04))"
        layers.append(ball(f"{px:g} + {rr}*sin({ang})", f"{rr}*cos({ang})", 0, f"0.11*{on}", 8, notes={"track": nm, "past": 2, "ahead": 0}, count=24,
                           **glow(col, f"(0.9 + 1.6*exp(0 - 6*max(note.age, 0)))*{on}")))
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.45, 0.016, 0.6)]}


@idiom(needs=0, fam="count")
def haul(c):
    """Slack taken up. One part pulls on the bar line; another answers late (or early), by
    less each time, until they pull together. Each answer is a rope between two posts, the
    pull's at the left and the answer's at the right, and it hangs by as much as the answer
    was late: a knot on it for every sixteenth of slack. When the pull comes its post is
    struck and a light sets off along the rope; it reaches the far post as the answer is
    made (an early answer sends it the other way). The last rope is taut: both posts are
    struck at once, and it hums. Ropes still to come hang dim."""
    R = getattr(c, "haul", None)
    if not R:
        raise ValueError("no slack is taken up here")
    rows = R[0]
    n_ = len(rows)
    now = "(time.beat*4)"
    big = max(abs(r[2]) for r in rows) or 1
    gap = min(1.3, 4.5 / n_)
    x0, x1 = -3.5, 3.5
    layers = []
    for k, (pull, hl, slack, _) in enumerate(rows):
        y = ((n_ - 1) / 2 - k) * gap + 0.3 * gap           # (a rope hangs below its posts)
        late = slack >= 0
        start, end = (pull, hl) if late else (hl, pull)
        sag = 0.7 * gap * abs(slack) / big
        col = c.a if late else c.b
        come = f"step({start:g}, {now})"
        struck = lambda at: f"exp(0 - 0.5*max({now} - {at:g}, 0))*step({at:g}, {now})"      # noqa: E731
        rope = {"type": "beam", "from": [x0, y, 0], "to": [x1, y, 0], "sag": sag, "width": 0.032, "samples": 64, "color": col,
                "glow": f"0.38 + 0.85*{come} + 1.5*{struck(end)}"}
        if abs(slack) < 0.5:
            # (a taut rope hums when it is struck, for a bar or two; a slack one cannot)
            rope.update(wave=f"0.2*exp(0 - 0.032*max({now} - {end:g}, 0))*step({end:g}, {now})", waves=3, speed=5, samples=96,
                        glow=f"0.2 + 0.7*{come} + 1.5*exp(0 - 0.04*max({now} - {end:g}, 0))*step({end:g}, {now})")
        layers.append(rope)
        m = round(abs(slack))
        if m:
            f_ = f"((inst.i + 1)/{m + 1})"
            layers.append(ball(f"{n(x0)} + {x1 - x0:g}*{f_}", f"{n(y)} - {sag * 4:g}*{f_}*(1 - {f_})", -0.02, min(0.06, 2.2 / (m + 1)), 8, count=m, **glow(col, f"0.3 + 1.2*{come}")))
        for x, at in ((x0, pull), (x1, hl)):
            layers.append(box(x, y, 0, 0.045, 0.2 * gap, 0.02, **glow(c.ink, f"0.3 + 2.4*{struck(at)}")))
        if m:
            t = f"clamp(({now} - {start:g})/{max(end - start, 0.01):g}, 0, 1)"
            u = t if late else f"(1 - {t})"
            on = f"step({start:g}, {now})*step({now}, {end + 1.5:g})"
            layers.append(ball(f"{n(x0)} + {x1 - x0:g}*{u}", f"{n(y)} - {sag * 4:g}*{u}*(1 - {u})", -0.05, f"0.12*{on}", 10, **glow("#ffffff", f"1.8*{on}")))
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.45, 0.016, 0.7)]}


@idiom(needs=0, fam="count")
def periods(c):
    """A tune in which every note lasts as long as its period. Each note is one wave, as long
    as the note lasts and as high as it is long, so that every wave is the same wave at
    another size: the low notes are the big waves and the high notes the small ones, and the
    higher a note stands the shorter it is. A wave is drawn as its note sounds, by a point
    that rides it. Under the tune runs a ruler with a mark for every count of the song, each
    mark in the colour of the note that holds it and lit as it is counted, and a taller
    mark where a note begins. The frame holds the stretch of the tune the scene plays and a
    bar to either side."""
    R = getattr(c, "periods", None)
    if not R:
        raise ValueError("no tune of periods here")
    _, A, B, grid, rows = R
    g0 = rows[0][0]
    a, b = max(A, c.a16 - 8), min(B, c.b16 + 8)
    if b - a < 48:
        a = max(A, min(a, b - 48))
        b = min(B, max(b, a + 48))
    rows = [r for r in rows if r[0] >= a - 0.01 and r[0] + r[1] <= b + 0.01]
    if len(rows) < 4:
        raise ValueError("too little of the tune")
    now = "(time.beat*4)"
    wide = 7.9
    u = wide / max(b - a, 1)
    sizes_ = sorted({r[3] for r in rows}, reverse=True)
    keys = [r[2] for r in rows]
    lo, hi = min(keys), max(keys)
    big, small = max(r[1] for r in rows) * u, min(r[1] for r in rows) * u
    amp = min(0.5, 1.45 / max(big, 0.01))            # (a wave is this many times as high as it is long)
    top, base = 2.25, -1.45
    layers = []
    at = lambda key: base + big * amp + (top - small * amp - base - big * amp) * ((key - lo) / max(hi - lo, 1))  # noqa: E731
    for i, (on, w, key, n_) in enumerate(rows):
        x0, x1 = (on - a) * u - wide / 2, (on + w - a) * u - wide / 2
        col = c.col(sizes_.index(n_))
        h = amp * w * u
        y = at(key)
        reach = f"clamp(({now} - {on:g})/{w:g}, 0, 1)"
        wave = {"type": "beam", "from": [x0, y, 0], "to": [x1, y, 0], "wave": h, "waves": 2, "speed": 0, "samples": 40, "color": col}
        layers.append({**wave, "width": 0.018, "glow": 0.34})
        layers.append({**wave, "width": 0.045, "glow": f"0.9 + 1.6*exp(0 - 0.5*max({now} - {on + w:g}, 0))", "reach": reach})
        # (where the next note follows at once, a hair line carries the tune over to it)
        if i + 1 < len(rows) and abs(rows[i + 1][0] - (on + w)) < 0.3:
            layers.append({"type": "beam", "from": [x1, y, 0], "to": [x1, at(rows[i + 1][2]), 0], "width": 0.008, "glow": f"0.16 + 0.5*step({on + w:g}, {now})", "color": c.dim})
        # The point that draws it (there only while the note sounds).
        on_ = f"step({on:g}, {now})*step({now}, {on + w:g})"
        layers.append(ball(f"{n(x0)} + {x1 - x0:g}*{reach}", f"{n(y)} + {h:g}*sin({reach})", -0.05, f"0.1*{on_}", 10, **glow("#ffffff", f"1.6*{on_}")))
        # Its marks on the ruler: the counts of the song that fall in it, and a taller one where it begins.
        j0 = math.ceil((on - g0) / grid - 0.02)
        m = max(0, math.ceil((on + w - g0) / grid - 0.02) - j0)
        if m and grid * u > 0.03:
            lit = f"step({g0 + j0 * grid:g} + inst.i*{grid:g}, {now})"
            layers.append(box(f"{n((g0 + j0 * grid - a) * u - wide / 2)} + inst.i*{grid * u:g}", -2.13, 0, min(0.018, grid * u * 0.25), 0.07, 0.01, count=m, **glow(col, f"0.22 + 1.3*{lit}")))
        layers.append(box(x0, -2.04, -0.01, 0.012, 0.16, 0.01, **glow(col, f"0.3 + 1.4*step({on:g}, {now})")))
    cur = f"clamp(({now} - {a:g})/{max(b - a, 1):g}, 0, 1)*{wide:g} - {wide / 2:g}"
    layers.append(box(cur, -2.0, -0.03, 0.008, 0.26, 0.01, **glow(c.ink, 1.2)))
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.45, 0.016, 0.7)]}


@idiom(needs=0, fam="count")
def overtones(c):
    """Harmonic partials beating together: a row of resonant reeds or harmonic bars, one
    for each overtone partial of the beat (1x, 2x, 3x, 4x, 5x...), plus a live interference
    locus along the bottom where their waves add up. Each partial's actual notes send bright
    travelling pulses along its string and ring its resonator; where partials coincide on
    a beat, the interference trace swells bright."""
    R = getattr(c, "partials", None)
    if not R:
        raise ValueError("no harmonic partials here")
    r0, harms = R  # r0: fundamental notes/beat; harms: [(mult, track_name, rate), ...]
    harms = harms[:5]
    n_ = len(harms)
    gap = min(0.76, 3.3 / max(n_, 1))
    top_y = 2.05
    layers = []
    # Vertical beat grid lines across the harmonic staff.
    layers.append(box(f"(inst.i - 4)*1.05", 0.35, 0.06, 0.008, 1.85, 0.01, count=9, **glow(c.dim, "0.28 + 0.35*pow(1 - time.phase, 4)")))
    sum_terms = []
    env = {}
    for i, (mult, nm, rate) in enumerate(harms):
        y = top_y - (i + 0.5) * gap
        col = c.col(i)
        env[f"p{i}"] = {"on": f"track.{nm}", "attack": "4ms", "decay": "180ms"}
        # Resonant standing-wave string vibrating at `mult` half-waves, driven by its part.
        layers.append({
            "type": "beam",
            "from": [-3.95, y, 0.01],
            "to": [3.95, y, 0.01],
            "wave": f"(0.05 + 0.22*env.p{i})",
            "waves": mult,
            "speed": f"{rate * 0.5:g}",
            "width": 0.026,
            "samples": 72,
            "color": col,
            "glow": f"0.55 + 1.8*env.p{i}",
        })
        # Actual note attacks gliding across the string from right (now) to left (past 4 beats).
        tr = {"track": nm, "past": 4.0, "ahead": 0}
        x_note = "(3.95 - note.age*1.975)"
        fresh = "exp(0 - 4*max(note.age, 0))"
        layers.append(ball(x_note, y, -0.02, f"(0.06 + 0.09*{fresh})", 8, notes=tr, count=64,
                           **glow(col, f"(0.6 + 2.2*{fresh})*(1 - 0.65*clamp(note.age/4, 0, 1))")))
        # Left resonator bead pulsing on every attack of this partial.
        layers.append(ball(-4.12, y, -0.03, f"0.08 + 0.09*env.p{i}", 10, **glow(col, f"0.8 + 2.0*env.p{i}")))
        # Nodes along the harmonic string (mult - 1 interior nodes).
        if mult >= 2:
            layers.append(box(f"0 - 3.95 + (inst.i + 1)*{7.9 / mult:g}", y, 0.03, 0.012, 0.09, 0.01, count=mult - 1, **glow(c.ink, 0.75)))
        sum_terms.append(f"cos((inst.i/95 - 0.5)*{mult * 2:g} - time.beat*{rate:g})")
    # Combined beating waveform along the foot: constructive interference peaks glow bright.
    y_bot = -1.78
    wave_sum = "(" + " + ".join(sum_terms) + f")/{max(n_, 1)}"
    layers.append(box(0, y_bot, 0.04, 4.0, 0.008, 0.01, **glow(c.dim, 0.65)))
    layers.append(ball(f"0 - 3.95 + inst.i*{7.9 / 95:g}", f"{n(y_bot)} + 0.48*({wave_sum})", -0.02,
                       f"0.038 + 0.045*pow(abs({wave_sum}), 2)", 6, count=96,
                       **glow(c.ink, f"0.55 + 2.4*pow(abs({wave_sum}), 2)")))
    # Playhead bar on the right edge where new attacks arrive.
    hit_all = "env.p0"
    for i in range(1, n_):
        hit_all = f"max({hit_all}, env.p{i})"
    layers.append(box(3.95, 0.35, -0.04, 0.014, 1.85, 0.01, **glow("#ffffff", f"0.6 + 1.4*{hit_all}")))
    return {"background": c.bg, "camera": FLAT, "env": env, "layers": layers, "filters": [bloom(c, 0.45, 0.016, 0.7)]}


@idiom(needs=0, fam="count")
def septlock(c):
    """Seven notes to the beat locking onto the quarter-note pulse: a seven-toothed wheel
    turning once a beat, lit by every note of the riff as it strikes each seventh, with a
    four-beat bar ring outside it and the lock tooth flaring white where the riff closes
    onto the beat."""
    R = getattr(c, "sept", None)
    if not R:
        raise ValueError("no seven-to-the-beat lock here")
    parts = R[:3]  # track names playing 7-to-the-beat (e.g. gl, dl, wl)
    env = {f"s{i}": {"on": f"track.{nm}", "attack": "2ms", "decay": "130ms"} for i, nm in enumerate(parts)}
    layers = []
    # Outer 4-beat bar ring: 4 cardinal beat posts and a slow bar hand.
    bar_r = 2.18
    layers.append(ball(f"{bar_r:g}*sin(inst.i/120)", f"{bar_r:g}*cos(inst.i/120)", 0.04, 0.015, 4, count=120, **glow(c.dim, 0.9)))
    layers.append(box(f"{bar_r:g}*sin(inst.i/4)", f"{bar_r:g}*cos(inst.i/4)", 0.02, 0.045, 0.14, 0.01, count=4, rz="0 - inst.i/4",
                      **glow(c.ink, "0.65 + 1.6*pow(1 - time.phase, 4)")))
    bar_ph = "fract(time.beat/4)"
    layers.append({"type": "beam", "from": [0, 0, 0.02], "to": [f"{bar_r:g}*sin({bar_ph})", f"{bar_r:g}*cos({bar_ph})", 0.02],
                   "width": 0.02, "samples": 12, "color": c.dim, "glow": 0.9})
    # Concentric 7-toothed rings, one per playing voice, each completing one full turn per beat!
    radii = (1.62, 1.2, 0.8)
    for i, nm in enumerate(parts):
        rr = radii[i]
        col = c.col(i)
        # 7 fixed tooth sockets around the beat dial, tooth 0 at 12 o'clock (the beat lock).
        layers.append(ball(f"{rr:g}*sin(inst.i/7)", f"{rr:g}*cos(inst.i/7)", 0.01, 0.055 if i == 0 else 0.045, 6, count=7,
                           **glow(c.dim, "0.8 + 0.9*step(inst.i, 0.5)")))
        # Every actual note sits at its exact fractional position within the beat (fract(note.beat))
        # and lingers for 2 beats, showing the 7-tooth gear locking onto the 7 sockets!
        ang = "fract(note.beat + 0.001)"
        fresh = "exp(0 - 6*max(note.age, 0))"
        rad_n = f"({rr:g} + 0.18*(note.key - 0.15))"
        layers.append(ball(f"{rad_n}*sin({ang})", f"{rad_n}*cos({ang})", -0.02 - 0.01 * i,
                           f"(0.075 + 0.12*{fresh})*(1 - 0.4*clamp(note.age/2, 0, 1))", 8,
                           notes={"track": nm, "past": 2.0, "ahead": 0}, count=48,
                           **glow(col, f"(0.65 + 2.4*{fresh})*(1 - 0.7*clamp(note.age/2, 0, 1))")))
        # Spokes connecting centre to active beat phase.
        ph = "fract(time.beat)"
        layers.append({"type": "beam", "from": [0, 0, 0], "to": [f"{rr:g}*sin({ph})", f"{rr:g}*cos({ph})", 0],
                       "width": 0.028 if i == 0 else 0.018, "samples": 10, "color": col, "glow": f"0.5 + 1.6*env.s{i}"})
    # The lock anvil at 12 o'clock: flares white each time the 7-note cycle closes on the beat.
    lock_hit = "exp(0 - 7*time.phase)"
    layers.append(box(0, 1.92, -0.05, 0.06, 0.24, 0.02, **glow("#ffffff", f"0.5 + 2.8*{lock_hit}")))
    layers.append(ball(0, 0, -0.05, f"0.14 + 0.12*{lock_hit}", 12, **glow("#ffffff", f"0.7 + 2.2*{lock_hit}")))
    # Side step strip on left and right edges: 7 vertical notches counting the 7ths of the beat.
    for side in (-3.65, 3.65):
        here = "floor(fract(time.beat)*7)"
        layers.append(box(side, "(3 - inst.i)*0.54", 0, 0.28, 0.18, 0.01, count=7,
                          **glow(c.a if side < 0 else c.b, f"0.22 + 2.2*(1 - step(0.5, abs(inst.i - {here})))")))
    return {"background": c.bg, "camera": FLAT, "env": env, "layers": layers, "filters": [bloom(c, 0.45, 0.016, 0.65)]}


@idiom(needs=0, fam="count")
def recount(c):
    """A band recounting at 16:15 without changing tempo: two concentric dials side by side
    and a twin-track ruler below. The old sixteen-to-a-bar ruler keeps steady clock time
    while the band's new sixteen fits into fifteen of the old sixteenths, gaining a whole
    sixteenth every bar and visibly pulling ahead."""
    R = getattr(c, "recount", None)
    if not R:
        raise ValueError("no grid recount here")
    at16, unit, parts = R  # at16: sixteenth of change, unit: 0.9375 (15/16), parts: [track names]
    parts = parts[:3]
    now = "(time.beat*4)"
    elapsed = f"max({now} - {at16:g}, 0)"
    old_ph = f"fract({elapsed}/16)"
    new_ph = f"fract({elapsed}/{16 * unit:g})"
    env = {f"r{i}": {"on": f"track.{nm}", "attack": "4ms", "decay": "160ms"} for i, nm in enumerate(parts)}
    layers = []
    # Left dial: old 16-count bar; right dial: new 16-in-15 bar (faster hand).
    for cx, ph, col, label_r in ((-2.15, old_ph, c.ink, 1.35), (2.15, new_ph, c.a, 1.35)):
        layers.append(ball(f"{n(cx)} + {label_r:g}*sin(inst.i/16)", f"0.45 + {label_r:g}*cos(inst.i/16)", 0,
                           "0.055 + 0.04*(1 - step(0.5, fract(inst.i/4)*4))", 6, count=16, **glow(col, "0.95 + 0.8*(1 - step(0.5, fract(inst.i/4)*4))")))
        layers.append(ball(f"{n(cx)} + {label_r:g}*sin(inst.i/96)", f"0.45 + {label_r:g}*cos(inst.i/96)", 0.02, 0.015, 4, count=96, **glow(col, 0.65)))
        layers.append({"type": "beam", "from": [cx, 0.45, -0.02],
                       "to": [f"{n(cx)} + {label_r * 0.94:g}*sin({ph})", f"0.45 + {label_r * 0.94:g}*cos({ph})", -0.02],
                       "width": 0.046, "samples": 12, "color": col, "glow": 1.85})
        layers.append(ball(cx, 0.45, -0.03, 0.11, 8, **glow(col, 1.6)))
    # Centre bridge showing the live phase slip between old count and new count.
    slip = f"fract({elapsed}/{16 * unit:g} - {elapsed}/16)"
    layers.append({"type": "beam", "from": [-0.65, 0.45, 0], "to": [0.65, 0.45, 0],
                   "wave": f"0.12 + 0.45*sin({slip})", "waves": 2, "speed": 2, "width": 0.03, "samples": 36, "color": c.b, "glow": 1.4})
    layers.append(ball(0, f"0.45 + 1.15*({slip} - 0.5)", -0.04, 0.11, 10, **glow("#ffffff", 1.8)))
    # Twin vernier ruler along the bottom: 16 old sixteenths vs 16 new (15/16) sixteenths,
    # with live note attacks plotted straight onto the moving new ruler!
    w = 7.8
    for idx in range(16):
        xo = -w / 2 + idx * (w / 16)
        xn = -w / 2 + idx * (w / 16) * unit
        layers.append(box(xo, -1.35, 0.01, 0.022, 0.2 if idx % 4 == 0 else 0.11, 0.01, **glow(c.ink, 1.15)))
        layers.append(box(xn, -1.85, 0.01, 0.024, 0.2 if idx % 4 == 0 else 0.11, 0.01, **glow(c.a, 1.35)))
    # Travelling needles along both rulers + actual note markers from the recounting parts.
    layers.append(box(f"0 - {w / 2:g} + {w:g}*{old_ph}", -1.35, -0.02, 0.028, 0.28, 0.01, **glow(c.ink, 1.7)))
    layers.append(box(f"0 - {w / 2:g} + {w * unit:g}*{new_ph}", -1.85, -0.02, 0.032, 0.28, 0.01, **glow("#ffffff", 2.0)))
    for i, nm in enumerate(parts):
        col = c.col(i)
        nph = f"fract((note.beat*4 - {at16:g})/{16 * unit:g})"
        fresh = "exp(0 - 4*max(note.age, 0))"
        layers.append(ball(f"0 - {w / 2:g} + {w * unit:g}*{nph}", -1.85 - 0.22 * i, -0.04,
                           f"0.065 + 0.08*{fresh}", 8, notes={"track": nm, "past": 3.75, "ahead": 0}, count=48,
                           **glow(col, f"0.75 + 2.4*{fresh}")))
    return {"background": c.bg, "camera": FLAT, "env": env, "layers": layers, "filters": [bloom(c, 0.45, 0.016, 0.7)]}


@idiom(needs=0, fam="count")
def palindrome(c):
    """One strip of attacks read forwards and back simultaneously: two parallel tape tracks
    sliding opposite ways across a central reading head, one carrying the left hand forward
    and the other carrying the right hand reversed, with glowing bridge arcs snapping
    between them whenever mirrored strokes cross the head together."""
    R = getattr(c, "palin", None)
    if not R:
        raise ValueError("no forward/reverse pair here")
    pl, pr = R
    cell = pl.cell or 19
    u = 8.4 / cell
    env = {"pl": {"on": f"track.{pl.name}", "attack": "3ms", "decay": "180ms"},
           "pr": {"on": f"track.{pr.name}", "attack": "3ms", "decay": "180ms"}}
    layers = [
        # Central mirror axis / reading head.
        box(0, 0, -0.05, 0.018, 2.35, 0.01, **glow("#ffffff", "0.55 + 1.5*max(env.pl, env.pr)")),
        # Upper and lower tape rails, notched in sixteenths of the cell.
        box(0, 0.82, 0.05, 4.3, 0.012, 0.01, **glow(c.dim, 0.7)),
        box(0, -0.82, 0.05, 4.3, 0.012, 0.01, **glow(c.dim, 0.7)),
        box(f"(inst.i - {(cell - 1) / 2:g})*{u:g}", 0.82, 0.04, 0.01, 0.08, 0.01, count=cell, **glow(c.dim, 0.75)),
        box(f"(inst.i - {(cell - 1) / 2:g})*{u:g}", -0.82, 0.04, 0.01, 0.08, 0.01, count=cell, **glow(c.dim, 0.75)),
    ]
    # Top tape (left hand): flows right-to-left (past on left, upcoming on right).
    xl = f"(0 - note.age*4*{u:g})"
    fl = "exp(0 - 4*abs(note.age))"
    layers.append(box(xl, "0.82 + 0.55*(note.key - 0.15)", -0.01, max(u * 0.36, 0.05), f"0.16 + 0.35*{fl}", 0.01,
                      notes={"track": pl.name, "past": cell / 8, "ahead": cell / 8}, count=64,
                      **glow(c.a, f"(0.5 + 2.2*{fl})*step(abs(note.age), {cell / 8:g})")))
    # Bottom tape (right hand): flows left-to-right (mirror of time: past on right, upcoming on left).
    xr = f"(note.age*4*{u:g})"
    fr = "exp(0 - 4*abs(note.age))"
    layers.append(box(xr, "-0.82 - 0.55*(note.key - 0.15)", -0.01, max(u * 0.36, 0.05), f"0.16 + 0.35*{fr}", 0.01,
                      notes={"track": pr.name, "past": cell / 8, "ahead": cell / 8}, count=64,
                      **glow(c.b, f"(0.5 + 2.2*{fr})*step(abs(note.age), {cell / 8:g})")))
    # Live bridge beam connecting the two reading heads; glows brightest when both hands strike together.
    both = "min(env.pl, env.pr)"
    layers.append({"type": "beam", "from": [0, 0.82, -0.03], "to": [0, -0.82, -0.03],
                   "wave": f"0.08 + 0.35*{both}", "waves": 3, "speed": 4, "width": f"0.025 + 0.05*{both}",
                   "samples": 36, "color": c.ink, "glow": f"0.4 + 2.6*{both}"})
    # Orbiting counter-turning indicator rings showing left's forward turn and right's backward turn.
    layers.append(ball(f"0 - 3.55 + 0.52*cos({pl.turn})", f"1.75 + 0.52*sin({pl.turn})", 0, 0.08, 8, **glow(c.a, f"0.9 + 1.4*env.pl")))
    layers.append(ball(f"3.55 + 0.52*cos(0 - {pr.turn})", f"-1.75 + 0.52*sin(0 - {pr.turn})", 0, 0.08, 8, **glow(c.b, f"0.9 + 1.4*env.pr")))
    return {"background": c.bg, "camera": FLAT, "env": env, "layers": layers, "filters": [bloom(c, 0.45, 0.016, 0.7)]}


# ───────────────────────── grounds: the rest of the band, dimly ─────────────────────────

GROUNDS = ("halo", "footlights", "stars", "floor", "plasma", "smoke", "scope", "skyline", "ripples", "horizon")
# Pictures that leave most of the frame dark and are drawn straight onto it (nothing kept from
# frame to frame, no room or sky of their own): these may stand on a ground.
GROUNDED = set("searchlights solkattu numerals hailstone membrane mobile pong combs star tesla breakout armillary tally crystal strange teletype odometer loom slack hourglass metro bifurcate turtle fractal fireworks tetris moons "
               "lanterns kelvin constellation sonar treerings strings harmonograph contour letters keys abacus splitflap helix epicycle quad stringart remainder spiral "
               "orrery pendwave sunflower juggle radial clockshop venn switchboard star rain fountain echoes skein coins fan invaders golden fireflies candles".split())
# Guises a grounded picture may wear (they leave a dim ground a dim ground).
GROUND_OK = set("solar stop combed blown plain kaleido mirror wall planet tunnel echo slices fringe spin roll wound water torn hole lines warp falling ball tracking screen delayed puzzle smoked dripping "
                "coiled halves reeded louvers hyperbolic standing".split())


def ground(c, look, kind):
    """A living ground behind a picture that leaves most of the frame dark: what the picture
    does not show of the band (the kick, the snare, the hats, the sound itself), dimly, so
    the dark is somewhere. It is laid under everything the picture draws."""
    if not kind or "layers" not in look:
        return look
    kick = c.kick.hit if getattr(c, "kick", None) else "audio.low"
    snare = c.snare.hit if getattr(c, "snare", None) else "audio.onset"
    hat = c.hat.hit if getattr(c, "hat", None) else "audio.high"
    black = "#000000"
    g = {
        # A glow behind the middle that swells with the kick.
        "halo": [{"type": "gradient", "radial": 1, "palette": [c.a, black], "spread": 0.5, "light": f"0.10 + 0.22*{kick}", "blend": "add", "res": 0.25}],
        # Light coming up from under the frame, lifted by the sound.
        "footlights": [{"type": "gradient", "radial": 1, "y": -1.45, "palette": [c.b, black], "spread": 0.42, "light": f"0.16 + 0.5*audio.level + 0.2*{kick}", "blend": "add", "res": 0.25}],
        # Stars the hats set twinkling; the kick shoves the view on.
        "stars": [{"type": "stars", "count": 700, "speed": f"0.012 + 0.09*{kick}", "size": 1.3, "light": f"0.45 + 0.5*{hat}", "twinkle": 0.7, "streak": 1.5, "blend": "add"}],
        # A ruled floor going away under the picture, a line a beat.
        "floor": [{"type": "grid", "horizon": -0.12, "speed": "0.5*time.bpm", "density": 8, "width": 0.05, "depth": 1.4, "color": c.dim, "opacity": f"0.22 + 0.3*{kick}", "blend": "add"}],
        # A slow field in the picture's two colours that the sound stirs.
        "plasma": [{"type": "plasma", "palette": [black, c.a, black, c.b], "scale": 1.2, "speed": "0.04 + 0.5*audio.level", "warp": 0.8, "shade": 0.8, "light": 0.16, "res": 0.25, "blend": "add"}],
        # Smoke lying in the room, lit a little by the snare.
        "smoke": [{"type": "noise", "palette": [black, black, c.dim, black], "spread": 1, "scale": 1.0, "speed": 0.07, "warp": 0.9, "octaves": 3, "light": f"0.2 + 0.3*{snare}", "res": 0.25, "blend": "add"}],
        # The sound itself, round the picture.
        "scope": [{"type": "scope", "mode": "circle", "size": 3.3, "gain": 0.5, "width": 0.003, "glow": 0.6, "color": c.dim, "opacity": 0.6, "points": 1024, "blend": "add"},
                  {"type": "scope", "mode": "circle", "size": 2.2, "gain": 0.35, "width": 0.002, "color": c.a, "opacity": 0.3, "points": 1024, "rotate": 0.25, "blend": "add"}],
        # The sound's bands along the foot, like a town at night.
        "skyline": [{"type": "spectrum", "mode": "bars", "bands": 48, "height": 0.42, "y": -1.0, "size": 3.56, "fill": 0.82, "floor": 0.1, "color": c.dim, "opacity": 0.55, "blend": "add"}],
        # Rings going out from the middle, a ring a beat, brighter on the snare.
        "ripples": [{"type": "shape", "repeat": 4, "sides": 0, "radius": "0.05 + 2.1*fract(time.beat/4 + inst.i/4)", "width": 0.006, "fill": 0, "x": 0, "y": 0, "color": c.a,
                     "opacity": f"(0.16 + 0.4*{snare})*(1 - fract(time.beat/4 + inst.i/4))", "blend": "add"}],
        # A band of light lying across the frame, like the last of a day; the kick lifts it.
        "horizon": [{"type": "gradient", "angle": 0.25, "palette": [black, black, c.b, c.a, black, black, black], "spread": 1, "light": f"0.13 + 0.25*{kick}", "blend": "add", "res": 0.25}],
    }[kind]
    out = dict(look)
    out["layers"] = g + list(look["layers"])
    return out


# Pictures that are dim as they stand (rooms at night, things on black): their shadows are
# lifted before they are printed in the paper or made of small copies of themselves.
DIM = set("gallery cinema railway doors cradle ropes highway press golden venn kit globe ferris skyline lanterns candles coins sympathy "
          "puppet storm keys sonar belfry clockshop strobe inset balance contour helix tetris crystal searchlights hands splitflap "
          "fountain fireworks hammers turtle trampoline pong sunflower fan membrane torusknot".split())

# ───────────────────────── pictures of pictures ─────────────────────────

SMALL = ("spiral", "sunflower", "stringart", "moire", "strings", "clockshop", "combs", "vortex", "epicycle", "harmonograph", "mandala", "table", "tally", "slack", "sonar", "remainder", "kelvin", "chladni")


def _small(c, i, skip=()):
    """A small picture for part i: the i-th idiom of SMALL that fits it (rotated by the scene)."""
    order = SMALL[(c.seed + i * 5) % len(SMALL):] + SMALL[:(c.seed + i * 5) % len(SMALL)]
    for k in (0, 1):
        d = c.sub(i, 2 if k == 0 else 1)
        for name in order:
            info = REG[name]
            if name in skip or info["needs"] > len(d.riffs):
                continue
            try:
                return name, info["f"](d)
            except (ValueError, IndexError, TypeError, ZeroDivisionError):
                continue
    raise ValueError("nothing small fits")


@idiom(needs=2, fam="sheet", cost=3)
def quad(c):
    """Four pictures at once, each a different instrument reading one of the parts."""
    layers, used = [], []
    for k in range(4):
        name, look = _small(c, k % max(len(c.riffs), 1), skip=used)
        used.append(name)
        layers.append({"type": "actor", "use": look, "x": (-0.889, 0.889)[k % 2], "y": (0.5, -0.5)[k // 2], "scale": 0.49, "key": 0, "mask": "rect"})
    return {"background": "#000000", "layers": layers, "filters": []}


@idiom(needs=1, fam="sheet", cost=3)
def inset(c):
    """One picture whole, and in its corner another reading of the same riff."""
    try:
        n1, big = _small(c, 0, skip=[n for n in SMALL if n in THIN])      # (the whole one is a picture that fills its frame)
    except ValueError:
        n1, big = _small(c, 0)
    n2, small = _small(c, 1 if len(c.riffs) > 1 else 0, skip=[n1])
    corner = ((1.12, -0.6), (-1.12, -0.6), (1.12, 0.6), (-1.12, 0.6))[c.seed % 4]
    layers = [{"type": "actor", "use": big, "x": 0, "y": 0, "scale": 1, "key": 0, "mask": "none"},
              {"type": "actor", "use": small, "x": corner[0], "y": corner[1], "scale": 0.34, "key": 0, "mask": "rect"}]
    return {"background": "#000000", "layers": layers, "filters": []}


@idiom(needs=1, fam="room", cost=3)
def gallery(c):
    """A dark room with pictures on the wall, each a different instrument reading a part;
    someone stands before them."""
    layers = [lamp(0, 4, -3, 1.1), floor(c, 0, "#16161a", 0.25), box(0, 2, 3.05, 9, 2.2, 0.05, **solid("#2c2c33", 0.9))]
    used = []
    for k in range(3):
        name, look = _small(c, k % max(len(c.riffs), 1), skip=used)
        used.append(name)
        x = (k - 1) * 3.3
        layers.append({"type": "screen", "use": look, "x": x, "y": 1.75, "z": 3.0, "w": 2.9, "h": 1.63, "glow": 1.6, "res": 270})
        layers.append(lamp(x, 1.7, 1.6, 0.5, c.col(k), 4))
    layers.append({"type": "figure", "rig": "human", "motion": "sway", "energy": 0.3, "x": "2.2*sin(time.bar/12)", "y": 1.0, "z": 1.3, "scale": 0.95, "ry": 0.5, "color": "#060608", "light": 0.15, "ambient": 0.05, "rim": 0})
    return {"background": "#060608", "camera": cam("1.6*sin(time.bar/10)", 1.5, -3.2, look=("1.0*sin(time.bar/10)", 1.55, 3), zoom=1.9), "layers": layers,
            "filters": [{"type": "reflect", "y": 0, "amount": 0.35}, {"type": "tonemap", "knee": 0.75}, {"type": "aa"}, bloom(c, 0.3, 0.02, 0.8)]}


@idiom(needs=1, fam="room", cost=3)
def cinema(c):
    """A picture house: one of the film's own pictures on the screen, the beam overhead, and
    a row of heads."""
    name, look = _small(c, 0)
    layers = [{"type": "screen", "use": look, "x": 0, "y": 2.3, "z": 5, "w": 6.8, "h": 3.83, "glow": 1.55, "res": 360},
              box(0, 2.3, 5.1, 3.6, 2.1, 0.05, **solid("#16161a", 0.9)), lamp(0, 2.3, 3.0, 0.8, c.a, 8),
              {"type": "motes", "mode": "drift", "count": 200, "w": 4, "h": 2, "d": 8, "y": 2.8, "z": 0.5, "fall": 0.02, "wobble": 0.1, "size": 0.008, "glow": 0.4, "twinkle": 0.6, "color": "#cfd8ff"}]
    for row in range(2):
        nn = 8 - row
        layers.append({"type": "figure", "rig": "human", "motion": "none", "count": nn, "x": f"(inst.i - {(nn - 1) / 2})*0.95 + {0.45 * row}", "y": 0.55 - 0.25 * row, "z": 0.6 - 1.3 * row, "scale": 1.0, "ry": 0.5,
                       "color": "#020203", "light": 0.12, "ambient": 0.02, "rim": 0, "pose": {"head": [0, f"0.03*sin(time.bar/3 + inst.i*0.37)", 0]}})
    return {"background": "#020203", "camera": cam("0.3*sin(time.bar/12)", 1.6, -5.0, look=(0, 2.0, 5), zoom=2.2), "layers": layers, "filters": [{"type": "tonemap", "knee": 0.8}, {"type": "aa"}, bloom(c, 0.3, 0.02, 0.8)]}


@idiom(needs=2, fam="space", cost=3)
def portals(c):
    """Architectural triptych of live 3D portals in space: three angled monolith screens
    hovering above a dark reflective floor, each showing a live scene driven by its own
    voice, pivoting subtly on the beat as the camera glides between them."""
    P = c.riffs[:3]
    while len(P) < 3:
        P.append(P[0])
    used = []
    layers = [
        lamp(0, 5.2, -3.5, 1.0),
        lamp(-3.0, 2.2, -1.0, 0.55, c.a, 10),
        lamp(3.0, 2.2, -1.0, 0.55, c.b, 10),
        floor(c, 0, "#141826", 0.34),
    ]
    specs = [(-2.85, 1.55, 1.5, 0.065), (0.0, 1.72, 2.35, 0.0), (2.85, 1.55, 1.5, -0.065)]
    for k, (px, py, pz, ry0) in enumerate(specs):
        p_k = P[k]
        name, look = _small(c, k % max(len(c.riffs), 1), skip=used)
        used.append(name)
        sway = f"{ry0:g} + 0.018*sin({p_k.turn}/2)"
        lift = f"{py:g} + 0.12*{p_k.hit}"
        layers.append(box(px, lift, pz + 0.08, 1.46, 0.86, 0.04, ry=sway, **glow(c.col(k), f"0.5 + 0.85*{p_k.hit}")))
        layers.append({"type": "screen", "use": look, "x": px, "y": lift, "z": pz, "w": 2.8, "h": 1.58, "ry": sway, "glow": 1.4, "res": 180})
        layers.append(lamp(px, py, pz - 1.1, f"0.55 + 0.35*{p_k.hit}", c.col(k), 5.5))
    return {
        "background": "#05070e",
        "camera": cam("1.0*sin(time.bar/8)", "1.35 + 0.18*cos(time.bar/10)", -4.0, look=("0.35*sin(time.bar/8)", 1.38, 2.0), zoom=1.68),
        "layers": layers,
        "filters": [{"type": "reflect", "y": 0, "amount": 0.58}, {"type": "tonemap", "knee": 0.78}, {"type": "aa"}, bloom(c, 0.35, 0.018, 0.75)],
    }


# ───────────────────────── pictures made of two ─────────────────────────
# Any two idioms can share the frame. Each is drawn as it would be alone (its own camera,
# its own plate), reading its own part, and the frame is divided by the music.

COMBOS = {}


def combo(name):
    def deco(f):
        COMBOS[name] = f
        return f
    return deco


def _act(look, x=0.0, y=0.0, scale=1.0, mask="none", **kw):
    return {"type": "actor", "use": look, "x": x, "y": y, "scale": scale, "key": 0, "mask": mask, **kw}


@combo("double")
def c_double(c, A, B):
    """A double exposure: both pictures on the one plate."""
    return {"background": "#000000", "layers": [_act(A), _act(B, blend="screen", fade=0.85)], "filters": []}


@combo("intercut")
def c_intercut(c, A, B):
    """Cut back and forth between the two each time the lead riff comes round."""
    p = _lead(c)
    per = max(1, round(1.6 / c.six / (p.cell or 16)))
    on = f"step(0.5, fract(floor((time.beat*4 - {p.anchor:g})/{(p.cell or 16) * per})/2 + 0.25))"
    return {"background": "#000000", "layers": [_act(A, fade=f"1 - {on}"), _act(B, fade=on)], "filters": []}


@combo("window")
def c_window(c, A, B):
    """One picture whole, and a round window in it on the other, opening with the riff."""
    p = _lead(c)
    r = f"0.5 + 0.1*{p.hit}"
    return {"background": "#000000", "layers": [_act(A), {"type": "shape", "sides": 1, "radius": f"({r})*1.03", "width": 0, "fill": 1, "color": c.ink, "blend": "normal"},
                                                {"type": "shape", "sides": 1, "radius": f"({r})*1.0", "width": 0, "fill": 1, "color": "#000000", "blend": "normal"},
                                                _act(B, scale=f"({r})*1.0", mask="round")], "filters": []}


@combo("diptych")
def c_diptych(c, A, B):
    """Two pictures side by side, the middle of each filling its half of the frame."""
    return {"background": "#000000", "layers": [_act(A, x=-0.889, blend="normal", cut="half", cut_take=0), _act(B, x=0.889, blend="normal", cut="half", cut_take=1),
                                                box(0, 0, -0.1, 0.012, 2.6, 0.01, **glow(c.ink, 1))], "camera": FLAT, "filters": []}


def _two(c, A, B, **cut):
    """Both pictures whole, each shown in its own share of the frame."""
    return {"background": "#000000", "layers": [_act(A, blend="normal", cut_take=0, **cut), _act(B, blend="normal", cut_take=1, **cut)], "filters": []}


# Ways two readings of one riff are joined (a canon): in step every one of them is one whole
# picture; out of step the picture breaks along the joins, by as much as the parts are apart.
JOINS = ("half", "strips", "rings", "bands", "wedges", "board", "blocks", "ribs", "diagonal", "diamond", "spiral", "hex")


def canon(c, A, B, how):
    """One picture drawn for the part behind (A) and for the part ahead (B), joined `how`."""
    cell = _lead(c).cell or 16
    cut = {"half": dict(cut="half"),
           "strips": dict(cut="strips", cut_n=cell if 6 <= cell <= 16 else 8),
           "ribs": dict(cut="strips", cut_n=32),
           "bands": dict(cut="bands", cut_n=7),
           "rings": dict(cut="rings", cut_n=6),
           "wedges": dict(cut="wedges", cut_n=8, cut_at=0.0625),
           "board": dict(cut="checker", cut_n=6),
           "blocks": dict(cut="checker", cut_n=3),
           "diagonal": dict(cut="diagonal", cut_n=8),
           "diamond": dict(cut="diamond", cut_n=6),
           "spiral": dict(cut="spiral", cut_n=6, cut_at=0.08),
           "hex": dict(cut="hex", cut_n=8)}[how]
    return _two(c, A, B, **cut)


def flipped(look):
    """The picture the other way round, left to right."""
    return {**look, "filters": list(look.get("filters", [])) + [{"type": "tile", "cols": 1, "rows": 1, "x": 1, "flip": "mirror"}]}


def tug(c, A, B, pa, pb):
    """Two parts that answer one another: each has a picture, and the line between them is
    pushed across the frame by whichever is playing, as far as it plays for (so the frame
    keeps the account of who has had how much of the time)."""
    rate = 1.1 / c.bar_s
    look = {"background": "#000000",
            "env": {"ta": {"on": f"track.{pa.name}", "attack": "0ms", "decay": "600ms"}, "tb": {"on": f"track.{pb.name}", "attack": "0ms", "decay": "600ms"}},
            "vars": {"tug": {"integrate": f"{rate:.3f}*(max(track.{pa.name}.gate, step(0.25, env.ta)) - max(track.{pb.name}.gate, step(0.25, env.tb)))", "lo": -0.8, "hi": 0.8},
                     "line": {"follow": "var.tug", "attack": "120ms", "release": "120ms"}},
            "layers": [_act(A, blend="normal", cut="half", cut_at="var.line", cut_take=0), _act(B, blend="normal", cut="half", cut_at="var.line", cut_take=1),
                       box(f"{FW}*var.line", 0, -0.1, 0.012, 2.6, 0.01, **glow(c.ink, f"0.6 + 1.4*max(env.ta, env.tb)"))],
            "camera": FLAT, "filters": []}
    return look


def _step(p, per=1):
    """A count that goes up by one each time the riff comes round (sliding the last of the way)."""
    return f"(floor({p.turn}/{per}) + smooth(0.8, 1, fract({p.turn}/{per})))"


@combo("strips")
def c_strips(c, A, B):
    """The frame in as many upright strips as the riff has sixteenths, one picture in the odd
    ones and the other in the even; each time the riff comes round they change strips."""
    p = _lead(c)
    nn = p.cell or 16
    nn = nn if nn <= 16 else next((nn // k for k in (2, 3, 4) if nn % k == 0 and nn // k <= 16), 8)
    return _two(c, A, B, cut="strips", cut_n=nn, cut_at=_step(p))


@combo("bands")
def c_bands(c, A, B):
    """The same, lying down: bands across the frame, as many as the second riff has sixteenths (or six)."""
    p = c.riffs[1] if len(c.riffs) > 1 else _lead(c)
    nn = p.cell if p.cell and 3 <= p.cell <= 12 else 6
    return _two(c, A, B, cut="bands", cut_n=nn, cut_at=_step(p))


@combo("board")
def c_board(c, A, B):
    """A board of squares, one picture on the black and the other on the white; they change
    squares each time the riff comes round."""
    p = _lead(c)
    return _two(c, A, B, cut="checker", cut_n=(8, 6, 10, 4)[c.seed % 4], cut_at=_step(p))


@combo("wedges")
def c_wedges(c, A, B):
    """The frame cut like a cake into as many slices as the riff has sixteenths, turning a slice a turn."""
    p = _lead(c)
    nn = p.cell or 16
    nn = (nn if nn % 2 == 0 else nn * 2) if nn <= 12 else 8
    return _two(c, A, B, cut="wedges", cut_n=nn, cut_at=f"{_step(p)}/{nn}")


@combo("rings")
def c_rings(c, A, B):
    """Rings out from the middle, one picture and the other by turns, moving out a ring each time the riff comes round."""
    p = _lead(c)
    return _two(c, A, B, cut="rings", cut_n=(6, 8, 5, 10)[c.seed % 4], cut_at=_step(p))


@combo("triptych")
def c_triptych(c, A, B):
    """Three panels: the middle of one picture, with the middle of the other on either side of it."""
    return {"background": "#000000", "layers": [_act(A, x=-1.185, blend="normal", cut="strips", cut_n=3, cut_mod=3, cut_take=0), _act(B, blend="normal", cut="strips", cut_n=3, cut_mod=3, cut_take=1),
                                                _act(A, x=1.185, blend="normal", cut="strips", cut_n=3, cut_mod=3, cut_take=2),
                                                box("(inst.i - 0.5)*3.03", 0, -0.1, 0.012, 2.6, 0.01, count=2, **glow(c.ink, 1))], "camera": FLAT, "filters": []}


@combo("sweep")
def c_sweep(c, A, B):
    """One picture gives way to the other from left to right through the scene, and the line between them shows."""
    at = f"(2.2*{c.prog} - 1.1)"
    return {"background": "#000000", "layers": [_act(B, blend="normal"), _act(A, blend="normal", cut="half", cut_at=at, cut_take=1),
                                                box(f"{at}*4.545", 0, -0.1, 0.012, 2.6, 0.01, **glow(c.ink, 1))], "camera": FLAT, "filters": []}


@combo("satellite")
def c_satellite(c, A, B):
    """One picture whole; the other in a round window that goes round it once for each turn
    of the riff, and swells on its notes."""
    p = _lead(c)
    per = max(1, math.ceil(2.6 / ((p.cell or 16) * c.six)))
    u = f"({p.turn}/{per})"
    x, y = f"1.05*sin({u})", f"0.52*cos({u})"
    r = f"(0.3 + 0.07*{p.hit})"
    return {"background": "#000000", "layers": [_act(A), {"type": "shape", "sides": 1, "radius": f"{r}*1.04", "width": 0, "fill": 1, "color": c.ink, "blend": "normal", "x": x, "y": y},
                                                {"type": "shape", "sides": 1, "radius": r, "width": 0, "fill": 1, "color": "#000000", "blend": "normal", "x": x, "y": y},
                                                _act(B, x=x, y=y, scale=r, mask="round")], "filters": []}


@combo("nest")
def c_nest(c, A, B):
    """One picture, the other inside it, the first again inside that, and the second inside
    that; the frames breathe with the riff."""
    p = _lead(c)
    layers = []
    for k in range(4):
        sc = f"({0.62 ** k:.4f}*(1 + {0.03 * k:g}*{p.hit}))"
        if k:
            layers.append(box(0, 0, -0.1 * k, f"4.545*{sc} + 0.035", f"2.557*{sc} + 0.035", 0.01, **glow(c.ink if k % 2 else c.a, 1)))
        layers.append(_act(A if k % 2 == 0 else B, scale=sc, mask="rect" if k else "none", blend="normal"))
    return {"background": "#000000", "camera": FLAT, "layers": layers, "filters": []}


@combo("iris")
def c_iris(c, A, B):
    """One picture, and the other in an iris that is thrown wide open each time the riff
    comes round and closes again through the turn."""
    p = _lead(c)
    per = max(1, math.ceil(1.8 / ((p.cell or 16) * c.six)))
    r = f"(0.12 + 1.1*exp(0 - 3.2*fract({p.turn}/{per})))"
    return {"background": "#000000", "layers": [_act(A), {"type": "shape", "sides": 1, "radius": f"{r}*1.025", "width": 0, "fill": 1, "color": c.ink, "blend": "normal"},
                                                {"type": "shape", "sides": 1, "radius": r, "width": 0, "fill": 1, "color": "#000000", "blend": "normal"},
                                                _act(B, scale=r, mask="round")], "filters": []}


@combo("card")
def c_card(c, A, B):
    """One picture; the other is dealt over it like a card each time the riff comes round,
    from a different side each time, and taken away."""
    p = _lead(c)
    per = max(1, math.ceil(2.2 / ((p.cell or 16) * c.six)))
    u = f"fract({p.turn}/{per})"
    k = f"floor({p.turn}/{per})"
    away = f"(1 - smooth(0, 0.16, {u}) + smooth(0.8, 1, {u}))"      # 1 off the frame, 0 home
    side = f"(fract({k}/4)*4)"
    dx = f"(step({side}, 0.5) - step(1.5, {side})*step({side}, 2.5))"       # from the right, then (third) from the left
    dy = f"(step(0.5, {side})*step({side}, 1.5) - step(2.5, {side}))"       # from above, then (fourth) from below
    x, y = f"3.0*{away}*{dx}", f"1.7*{away}*{dy}"
    return {"background": "#000000", "camera": FLAT, "layers": [_act(A), box(f"2.557*({x})", f"2.557*({y})", -0.1, 4.545 * 0.66 + 0.035, 2.557 * 0.66 + 0.035, 0.01, **glow(c.ink, 1)),
                                                                _act(B, x=x, y=y, scale=0.66, mask="rect", blend="normal")], "filters": []}


@combo("glass")
def c_glass(c, A, B):
    """One picture seen through the other, which is made of glass: it bends what lies under
    it, and catches the light on its edges."""
    return {"background": "#000000", "layers": [_act(A), _act(B, **{"as": "lens", "bend": 0.09})], "filters": []}


@combo("stencil")
def c_stencil(c, A, B):
    """One picture shows only through the lights of the other, which is itself seen faintly."""
    return {"background": "#000000", "layers": [_act(A), _act(B, **{"as": "stencil", "gain": 5, "ground": True}), _act(B, blend="add", fade=0.22)], "filters": []}


@idiom(needs=2, fam="space", cost=3)
def depthstage(c):
    """True depth-interplay stage: two live instruments occupy a shared 3D actor stage where
    they orbit past one another in depth (passing in front of and behind each other with real
    occlusion as their riffs drift in and out of phase) while a gentle camera glides through."""
    # Prefer rich/broad small idioms so both orbiting planes hold strong visual weight.
    n1, look1 = _small(c, 0, skip=list(THIN))
    n2, look2 = _small(c, 1, skip=list(THIN) + [n1])
    A, B = c.riffs[0], c.riffs[1]
    per = max(2, math.ceil(6.0 / ((A.cell or 16) * c.six)))
    ph = f"({A.turn}/{per} + 0.125)"
    ph2 = f"({B.turn}/{max(2, math.ceil(6.0 / ((B.cell or 16) * c.six)))})"
    actors = [
        {"use": look1, "name": "a", "mask": "rect", "res": 0.65,
         "x": f"0.75*sin({ph})", "y": f"0.16*cos({ph})", "z": f"0.85 + 0.52*cos({ph})",
         "scale": f"0.86 + 0.08*{A.hit}", "rotate": f"0.025*sin({ph})"},
        {"use": look2, "name": "b", "mask": "rect", "res": 0.65,
         "x": f"0 - actor.a.x", "y": f"0.18*sin({ph2})", "z": f"1.7 - actor.a.z",
         "scale": f"0.84 + 0.08*{B.hit}", "rotate": f"0 - 0.025*sin({ph2})"},
    ]
    return {
        "background": c.bg,
        "layers": [
            {"type": "stars", "count": 450, "speed": 0.015, "size": 1.1, "light": 0.35, "twinkle": 0.5, "streak": 1.2, "blend": "add"},
            {"type": "stage", "blend": "normal",
             "camera": {"x": "0.14*actor.a.x", "y": "0.06*sin(time.bar/6)", "z": -1.1, "zoom": 1.22, "roll": "0.012*sin(time.bar/8)", "fog": 0.08},
             "actors": actors},
        ],
        "filters": [bloom(c, 0.3, 0.014, 0.75)],
    }


@idiom(needs=2, fam="field", cost=2)
def moirefield(c):
    """Interfering spacetime waves: two grids of luminous bars oriented along the two riffs'
    angles, pulsing and sliding at each riff's own cadence, creating living interference
    fringes that lock crisp when the two cycles coincide."""
    A, B = c.riffs[0], c.riffs[1]
    env = hit_env([A, B], "160ms")
    na = max(6, min(A.cell, 24))
    nb = max(6, min(B.cell, 24))
    layers = [
        # First lattice: tilted slightly positive, sliding one bar per turn of A.
        box(f"(inst.i - {(na - 1) / 2:g})*{8.6 / na:g} + {8.6 / na:g}*(fract({A.turn}) - 0.5)", 0, 0.02,
            0.032 + 0.015 * (na < 12), 2.8, 0.01, count=na, rz=f"0.04 + 0.06*sin({A.turn}/4)",
            **glow(c.a, f"0.55 + 1.2*env.h0")),
        # Second lattice: counter-tilted, sliding at B's turn; interference bands beat at |1/A - 1/B|.
        box(f"(inst.i - {(nb - 1) / 2:g})*{8.6 / nb:g} - {8.6 / nb:g}*(fract({B.turn}) - 0.5)", 0, 0.0,
            0.032 + 0.015 * (nb < 12), 2.8, 0.01, count=nb, rz=f"0 - 0.04 - 0.06*sin({B.turn}/4)",
            **glow(c.b, f"0.55 + 1.2*env.h1")),
        # Horizontal interference nodes where A and B phases agree.
        ball(f"3.4*sin({A.turn})", f"1.8*cos({B.turn})", -0.04, f"0.16 + 0.14*min(env.h0, env.h1)", 12,
             **glow("#ffffff", "0.7 + 2.5*min(env.h0, env.h1)")),
    ]
    return {"background": c.bg, "camera": FLAT, "env": env, "layers": layers,
            "filters": [{"type": "slitwave", "waves": 3, "amp": "0.02 + 0.05*max(env.h0, env.h1)", "phase": f"{A.turn}/2", "angle": 0.125, "split": 0.45},
                        bloom(c, 0.45, 0.016, 0.65)]}


@idiom(needs=2, fam="space", cost=2)
def phasecorridor(c):
    """Spacetime corridor: 24 luminous rectangular gates receding into depth along a curved
    track, each gate twisting by an integrated phase driven by the two riffs' hits so the
    corridor coils and uncoils dynamically as the phrase builds."""
    A, B = c.riffs[0], c.riffs[1]
    env = hit_env([A, B], "220ms")
    n_ = 24
    # Integrated phase accumulates twist on every note of A and counter-twist on B.
    vars_ = {
        "coil": {"integrate": f"0.12 + 0.55*{A.hit} - 0.35*{B.hit}"},
        "sway": {"follow": f"env.h0 - env.h1", "attack": "90ms", "release": "420ms"},
    }
    depth = "(fract(inst.i/24 - time.bar/8)*14)"
    x = f"(1.1*sin({depth}/6 + var.coil*0.25) + 0.6*var.sway*(1 - {depth}/14))"
    y = f"(0.7*cos({depth}/7 + {B.turn}/4))"
    rz = f"({depth}*0.045 + var.coil*0.18 + {A.turn}/4)"
    sc = f"(2.25 - 0.04*{depth} + 0.18*env.h0*step({depth}, 3.5))"
    layers = [
        {"type": "stars", "count": 400, "speed": 0.2, "size": 0.85, "light": 0.5, "twinkle": 0.3, "streak": 1.6},
        {"type": "mesh", "shape": "torus", "detail": 4, "count": n_, "x": x, "y": y, "z": depth,
         "scale": sc, "tube": 0.036, "rx": 0.25, "rz": rz,
         **glow(c.a, f"(0.45 + 1.4*env.h0)*(1 - {depth}/15)")},
        {"type": "mesh", "shape": "torus", "detail": 4, "count": n_, "x": f"0 - ({x})*0.5", "y": f"0 - ({y})*0.5", "z": f"({depth}) + 0.3",
         "scale": f"({sc})*0.64", "tube": 0.024, "rx": 0.25, "rz": f"0 - ({rz})",
         **glow(c.b, f"(0.4 + 1.3*env.h1)*(1 - {depth}/15)")},
        # Central rhythmic beacon ahead at the vanishing point.
        ball("0.5*sin(var.coil*0.3)", "0.35*cos(var.coil*0.25)", 13.5, "0.45 + 0.3*max(env.h0, env.h1)", 14,
             **glow(c.ink, "1.1 + 2.2*min(env.h0, env.h1)")),
    ]
    return {
        "background": c.bg,
        "env": env,
        "vars": vars_,
        "camera": cam("0.35*var.sway", "0.15*sin(time.bar/6)", -1.6, look=("0.4*sin(var.coil*0.2)", 0, 8), zoom=1.15, roll="0.03*var.sway"),
        "layers": layers,
        "filters": [{"type": "fog", "amount": 1.0, "density": 0.085, "color": c.bg}, {"type": "aa"}, bloom(c, 0.45, 0.018, 0.65)],
    }


@idiom(needs=1, fam="grow", cost=2)
def mycelium(c):
    """A growth fed by the riffs. Every note lays food at its place in its riff's turn round
    a ring (a ring to a riff, the longest riff's the widest), and a net of threads that
    follow one another draws itself between them: each riff as the shortest ways between
    its own notes, and bridges from ring to ring that are redrawn as the riffs slip past
    one another."""
    P = sorted(c.riffs[:3], key=lambda p: -(p.cell or 16))
    radii = ([0.62], [0.8, 0.4], [0.84, 0.52, 0.22])[len(P) - 1]
    env = hit_env(P, "200ms")
    lay = {"type": "mycelium", "size": 200, "agents": 18000, "rate": 54, "sense": 0.03, "angle": 0.075, "turn": 0.1, "decay": 0.86, "gain": 0.75,
           "food": 1.4, "linger": round(min(6.0, max(0.9, (P[0].cell or 16) * c.six * 0.95)), 2), "radius": 0.03, "spread": 0.75,
           "burst": 0.05, "thick": 3.0, "seed": c.seed % 997, "palette": [c.dim, c.a, c.ink]}
    marks = []
    for i, (p, r) in enumerate(zip(P, radii)):
        x, y = f"{1.5 * r:g}*sin({p.turn})", f"{r:g}*cos({p.turn})"
        k = "" if i == 0 else str(i + 1)
        lay.update({f"on{k}": f"track.{p.name}", f"x{k}": x, f"y{k}": y})
        # Where each riff is in its turn: a point going round its ring.
        marks.append({"type": "shape", "sides": 1, "radius": f"0.014 + 0.03*env.h{i}", "width": 0, "fill": 1, "x": x, "y": y, "color": c.col(i), "opacity": f"0.5 + 0.5*env.h{i}"})
    return {"background": "#05070a", "env": env, "layers": [lay] + marks, "filters": [{"type": "tonemap", "knee": 0.75}, bloom(c, 0.3, 0.014, 0.7)]}


@idiom(needs=2, fam="field", cost=2)
def ripplebath(c):
    """Live 2D wave-equation interference tank: two orbiting exciters follow the two riffs'
    cycles and drop real physical waves on every note, reflecting off the tank walls into
    luminous caustic interference patterns."""
    A, B = c.riffs[0], c.riffs[1]
    env = hit_env([A, B], "160ms")
    x1, y1 = f"0.92*cos({A.turn}/2)", f"0.56*sin({A.turn}/2)"
    x2, y2 = f"0 - 0.92*cos({B.turn}/2 + 0.15)", f"0.56*sin({B.turn}/2 + 0.15)"
    layers = [
        {"type": "wavefield", "size": 108, "on": f"track.{A.name}", "on2": f"track.{B.name}",
         "x": x1, "y": y1, "x2": x2, "y2": y2, "speed": 0.40, "damping": 0.977,
         "strength": 0.78, "strength2": 0.78, "radius": 0.048, "gain": 1.35, "steps": 4,
         "spread": 0.9, "palette": [c.b, "#162d52", c.a, c.ink]},
        # Subtle glowing drop markers showing where each voice strikes the water.
        {"type": "shape", "sides": 1, "radius": "0.02 + 0.025*env.h0", "width": 0, "fill": 1,
         "x": x1, "y": y1, "color": c.a, "opacity": "0.45 + 0.55*env.h0"},
        {"type": "shape", "sides": 1, "radius": "0.02 + 0.025*env.h1", "width": 0, "fill": 1,
         "x": x2, "y": y2, "color": c.b, "opacity": "0.45 + 0.55*env.h1"},
    ]
    return {"background": "#060b16", "env": env, "layers": layers,
            "filters": [{"type": "tonemap", "knee": 0.72}, bloom(c, 0.34, 0.016, 0.7)]}


@idiom(needs=2, fam="knot", cost=2)
def torusknot(c):
    """Two riffs as the two ways round a ring: the long way round is one turn of the first
    riff, the short way, round the tube, one turn of the second. Now is a lamp going both
    ways at once, so its path winds round the ring, and every note is a bead left where the
    lamp was when it sounded. The first riff's notes stand in hoops round the tube and the
    second's in rings the long way round; the winding closes only when both come round
    together."""
    A, B = c.riffs[0], c.riffs[1]
    parts = _cast(c, 4)
    S, tube = 2.3, 0.4
    R, r = 0.75 * S, 0.75 * S * tube

    def at(t16, lift=0.0):
        """Where on the ring the sixteenth t16 (an expression) lies."""
        th = f"(({t16}) - {A.anchor:g})/{A.cell}"
        ph = f"(({t16}) - {B.anchor:g})/{B.cell}"
        rr = f"({R:g} + {r + lift:g}*cos({ph}))"
        return f"{rr}*cos({th})", f"{r + lift:g}*sin({ph})", f"{rr}*sin({th})"

    cyc = A.cell * B.cell // math.gcd(A.cell, B.cell)       # sixteenths until both come round
    long_ = max(A.cell, B.cell)
    back = min(2 * long_, 48)                               # the lamp's wake, in sixteenths
    layers = [{"type": "stars", "count": 300, "speed": 0, "size": 0.8, "light": 0.35, "twinkle": 0.2, "streak": 0},
              lamp(-4, 6, -5, 1.25), lamp(5, -2, -4, 0.55, c.a), lamp(0, 3, 6, 0.4, c.b),
              {"type": "mesh", "shape": "torus", "detail": 44, "x": 0, "y": 0, "z": 0, "scale": S * 0.985, "tube": tube * 0.97, **solid("#141b30", 0.55), "emit": 0.05},
              {"type": "mesh", "shape": "torus", "detail": 16, "mode": "wire", "x": 0, "y": 0, "z": 0, "scale": S, "tube": tube, "color": c.dim, "emit": 0.42, "light": 0, "ambient": 0, "rim": 0, "width": 1.0}]
    # The wake: the lamp's path over the last turns, thick at the lamp and thinning back.
    wx, wy, wz = at(f"time.beat*4 - (1 - vtx.u)*{back}", 0.03)
    layers.append({"type": "mesh", "shape": "path", "detail": max(20, min(60, round(back / min(A.cell, B.cell) * 9))), "path": [wx, wy, wz], "radius": "0.006 + 0.03*vtx.u*vtx.u",
                   "x": 0, "y": 0, "z": 0, "scale": 1, **glow(c.ink, f"0.9 + 1.2*{A.hit}")})
    # The way ahead, as far as the longer riff's next turn, faint.
    fx, fy, fz = at(f"time.beat*4 + vtx.u*{long_}", 0.03)
    layers.append({"type": "mesh", "shape": "path", "detail": 20, "path": [fx, fy, fz], "radius": 0.006, "x": 0, "y": 0, "z": 0, "scale": 1, **glow(c.dim, 0.7)})
    for i, p in enumerate(parts):
        bx, by, bz = at("note.beat*4", 0.035 + 0.03 * i)
        layers.append(ball(bx, by, bz, f"{0.074 - 0.007 * i:g}*(1 + 1.7*exp(0 - 3*note.age))", 8, notes={"track": p.name, "past": max(8, min(48, cyc / 4))},
                           **glow(c.col(i), "0.55 + 3*exp(0 - 1.6*note.age)")))
    lx, ly, lz = at("time.beat*4", 0.07)
    layers.append(ball(lx, ly, lz, f"0.1 + 0.05*{A.hit} + 0.05*{B.hit}", 12, **glow("#ffffff", 3.2)))
    if c.variant % 2 == 0:
        camera = cam("4.9*sin(time.bar/18)", "2.9 + 0.5*sin(time.bar/7)", "0 - 4.9*cos(time.bar/18)", look=(0, -0.6, 0), zoom=1.72)
    else:           # low, looking along the ring
        camera = cam("5.4*sin(time.bar/14)", "1.15 + 0.35*sin(time.bar/9)", "0 - 5.4*cos(time.bar/14)", look=(0, -0.1, 0), zoom=1.9)
    return {"background": "#03040a", "camera": camera, "layers": layers, "filters": [{"type": "aa"}, bloom(c, 0.5, 0.02, 0.55)]}


@idiom(needs=1, fam="fill", paper=True, cost=2)
def hilbert(c):
    """Time laid over a square: a sixteenth is a cell, and the cells are taken along a
    Hilbert curve, so that what is near in time is near in space. A beat is a block of two
    by two, a bar a block of four by four, four bars a block of eight. Every note lights
    the cell it fell in. A riff a bar long prints the same figure in every block; a riff of
    another length prints one that never sits the same way twice. A square to a part."""
    P = _cast(c, 2, celled=True)
    if len(P) < 2:
        P = (P + [p for p in c.drums + c.every + c.tunes + c.parts if p.name not in {q.name for q in P}])[:2]
    order = 4 if (c.b16 - c.a16) >= 96 else 3               # sixteen bars to a square, or four
    side, cells = 2 ** order, 4 ** order
    S = 4.25                                                # the square's side
    u = S / side
    gap = 0.34
    now = f"(fract((time.beat*4 + 0.001)/{cells})*{cells})"
    layers = []
    for i, p in enumerate(P):
        x0 = (i - (len(P) - 1) / 2) * (S + gap)

        def at(d, x0=x0):
            return f"{x0:g} + (hilbx({d}, {order}) - {(side - 1) / 2:g})*{u:g}", f"({(side - 1) / 2:g} - hilby({d}, {order}))*{u:g}"
        col = c.col(i)
        # The ground, and the blocks of four by four (bars) ruled on it.
        layers.append(box(x0, 0, 0.3, S / 2 + 0.06, S / 2 + 0.06, 0.02, **glow(c.dim, 0.16)))
        for ax in (0, 1):
            n_ = side // 4 + 1
            xy = (f"{x0:g} + (inst.i - {(n_ - 1) / 2:g})*{4 * u:g}", 0) if ax == 0 else (x0, f"(inst.i - {(n_ - 1) / 2:g})*{4 * u:g}")
            sz = (0.006, S / 2) if ax == 0 else (S / 2, 0.006)
            layers.append(box(xy[0], xy[1], 0.25, sz[0], sz[1], 0.005, count=n_, **glow(c.dim, 0.75)))
        # The curve: a link from each cell to the next, lit as far as now has come this time round.
        mx, my = at("inst.i + 0.5")
        # (It runs over the lit cells, so the thread of time is seen going through the notes.)
        layers.append(box(mx, my, 0.04, f"0.0045 + {u / 2:g}*abs(hilbx(inst.i + 1, {order}) - hilbx(inst.i, {order}))", f"0.0045 + {u / 2:g}*abs(hilby(inst.i + 1, {order}) - hilby(inst.i, {order}))", 0.004,
                          count=cells - 1, **glow(c.ink, f"0.16 + 0.75*step(inst.i + 1, {now})")))
        # The notes: each lights its cell, bright as it sounds and settling to a steady lamp.
        d = f"floor(fract((note.beat*4 + 0.02)/{cells})*{cells})"
        nx, ny = at(d)
        layers.append(box(nx, ny, 0.1, f"{0.36 * u:g}*(1 + 0.45*exp(0 - 4*note.age))", f"{0.36 * u:g}*(1 + 0.45*exp(0 - 4*note.age))", 0.02,
                          notes={"track": p.name, "past": cells / 4 - 0.5}, **glow(col, "0.75 + 2.6*exp(0 - 1.2*note.age)")))
        # Now.
        cx_, cy_ = at(now)
        layers.append(box(cx_, cy_, 0, 0.5 * u, 0.5 * u, 0.02, **glow(c.ink, f"0.55 + 1.2*{p.hit}"), opacity=0.55))
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.4, 0.016, 0.6)]}


@idiom(needs=2, fam="spacetime", cost=2)
def worldlines(c):
    """Space one way and time the other. Each part goes round once in its riff, here and
    now, at the front; where it has been runs off behind it into the distance, so the past
    of each part is a coil as long as its riff, and the coils of two riffs cross where the
    riffs agree. Every note is a bead on its part's line, carried off into the past; the
    bar lines go with them along the floor."""
    parts = _cast(c, 4, celled=True)
    if len(parts) < 2:
        raise ValueError("one line")
    # Sixteenths of the past in view (two and a half turns of the longest riff), and how far off they run.
    span, deep = int(max(40, min(96, 2.5 * max(p.cell for p in parts)))), 12.0
    k = deep / span                                         # depth a sixteenth
    layers = [lamp(0, 6, 2, 0.55), floor(c, -1.7, "#0b0e1a", 0.35)]
    # Bar lines on the floor, running away at the speed of the past.
    layers.append(box(0, -1.69, f"(inst.i + fract(time.beat/4))*{16 * k:g}", 3.6, 0.004, 0.012, count=math.ceil(span / 16) + 1, **glow(c.dim, 0.7)))
    layers.append(box(0, -1.69, f"(inst.i + fract(time.beat))*{4 * k:g}", 0.5, 0.003, 0.008, count=span // 4 + 1, **glow(c.dim, 0.4)))
    for i, p in enumerate(parts):
        if len(parts) == 2:         # two coils, one inside the other: they cross where the riffs agree
            x0, amp, rise, y0 = 0, 2.5 - 0.7 * i, 0.6 + 0.2 * i, -0.3 + 0.3 * i
        else:                       # more: a coil to a lane, side by side, so their lengths are compared
            x0, amp, rise, y0 = (i - (len(parts) - 1) / 2) * 6.2 / len(parts), 2.5 / len(parts) + 0.2, 0.78, -0.45

        def at(t16, p=p, x0=x0, amp=amp, rise=rise, y0=y0):
            th = f"(({t16}) - {p.anchor:g})/{p.cell}"
            return f"{x0:g} + {amp:g}*sin({th})", f"{y0:g} + {rise:g}*cos({th})"
        wx, wy = at("time.beat*4 - vtx.u*%d" % span)
        layers.append({"type": "mesh", "shape": "path", "detail": max(14, min(60, math.ceil(span / p.cell * 5))), "path": [wx, wy, f"vtx.u*{deep:g}"],
                       "radius": "0.034 - 0.02*vtx.u", "x": 0, "y": 0, "z": 0, "scale": 1, **glow(c.col(i), f"0.75 + 0.8*{p.hit}")})
        bx, by = at("note.beat*4")
        layers.append(ball(bx, by, f"note.age*{4 * k:g}", "0.085*(1 + 1.6*exp(0 - 3*note.age))", 8, notes={"track": p.name, "past": span / 4},
                           **glow("#ffffff" if i == 0 else c.col(i), "0.9 + 2.6*exp(0 - 1.5*note.age)")))
        nx, ny = at("time.beat*4")
        layers.append(ball(nx, ny, 0, f"0.15 + 0.09*{p.hit}", 12, **glow(c.col(i), f"1.6 + 2*{p.hit}")))
    # Now: a frame the lines pass through.
    for sx_ in (-1, 1):
        layers.append(box(sx_ * 3.3, -0.2, 0, 0.012, 1.5, 0.012, **glow(c.ink, 0.55)))
    layers.append(box(0, 1.3, 0, 3.3, 0.012, 0.012, **glow(c.ink, 0.55)))
    side = 1 if c.variant % 2 == 0 else -1
    camera = cam(f"{side * -4.6:g} + 0.5*sin(time.bar/9)", "1.9 + 0.3*sin(time.bar/7)", -2.6, look=(side * 0.5, -0.4, 4.2), zoom=1.3)
    return {"background": "#04060d", "camera": camera, "layers": layers,
            "filters": [{"type": "reflect", "y": -1.7, "amount": 0.45}, {"type": "fog", "amount": 0.6, "density": 0.035, "color": "#04060d"}, {"type": "tonemap", "knee": 0.8}, {"type": "aa"}, bloom(c, 0.45, 0.018, 0.6)]}


@idiom(needs=2, fam="space", cost=3)
def kaleidohall(c):
    """Hall of mirrors: a receding 3D colonnade of six angled live-screen mirrors lining
    both sides of a glowing catwalk, showing two distinct voice scenes facing across the
    aisle while the camera glides down the corridor in time with the lead riff."""
    A, B = c.riffs[0], c.riffs[1]
    n1, look1 = _small(c, 0)
    n2, look2 = _small(c, 1, skip=[n1])
    layers = [
        lamp(0, 4.5, -2.0, 0.95),
        lamp(-2.5, 2.0, 2.5, 0.55, c.a, 10),
        lamp(2.5, 2.0, 2.5, 0.55, c.b, 10),
        floor(c, 0, "#0e1220", 0.3),
        # Central illuminated aisle strips counting out the riff.
        box(0, 0.015, f"(fract(inst.i/12 - {A.turn}/12)*10) - 1.0", 0.65, 0.008, 0.028, count=12,
            **glow(c.dim, f"0.35 + 0.9*{A.hit}")),
    ]
    # Three pairs of angled live-screen mirrors lining left (-x) and right (+x) walls,
    # each angled toward the aisle and viewer so every live scene reads clearly in perspective.
    for k in range(3):
        z = 0.9 + k * 2.6
        look_l, look_r = (look1, look2) if k % 2 == 0 else (look2, look1)
        p_l, p_r = (A, B) if k % 2 == 0 else (B, A)
        ry_l = f"0.115 + 0.015*sin({p_l.turn}/2 + {k * 0.25:g})"
        ry_r = f"-0.115 - 0.015*sin({p_r.turn}/2 + {k * 0.25:g})"
        # Left live screen + top/bottom glowing rails (never occludes screen face)
        layers.append({"type": "screen", "use": look_l, "x": -2.6, "y": 1.55, "z": z, "w": 2.45, "h": 1.48, "ry": ry_l, "glow": 1.5, "res": 160})
        for dy in (-0.77, 0.77):
            layers.append(box(-2.6, 1.55 + dy, z, 1.24, 0.024, 0.03, ry=ry_l, **glow(c.col(0), f"0.6 + 0.9*{p_l.hit}")))
        # Right live screen + top/bottom glowing rails
        layers.append({"type": "screen", "use": look_r, "x": 2.6, "y": 1.55, "z": z, "w": 2.45, "h": 1.48, "ry": ry_r, "glow": 1.5, "res": 160})
        for dy in (-0.77, 0.77):
            layers.append(box(2.6, 1.55 + dy, z, 1.24, 0.024, 0.03, ry=ry_r, **glow(c.col(1), f"0.6 + 0.9*{p_r.hit}")))
    # Far end portal framed at the vanishing point.
    layers.append(box(0, 1.75, 8.48, 1.78, 1.02, 0.04, **glow(c.ink, f"0.35 + 0.6*{A.hit}")))
    layers.append({"type": "screen", "use": look1, "x": 0, "y": 1.75, "z": 8.4, "w": 3.4, "h": 1.9, "glow": 1.45, "res": 180})
    return {
        "background": "#04060d",
        "camera": cam("0.55*sin(time.bar/6)", "1.35 + 0.15*cos(time.bar/8)", f"-2.6 + 1.2*sin({A.turn}/4)", look=("0.3*sin(time.bar/6)", 1.5, 6.0), zoom=1.55),
        "layers": layers,
        "filters": [{"type": "reflect", "y": 0, "amount": 0.55}, {"type": "fog", "amount": 0.65, "density": 0.045, "color": "#04060d"}, {"type": "tonemap", "knee": 0.78}, {"type": "aa"}, bloom(c, 0.35, 0.018, 0.72)],
    }


@combo("timemap")
def c_timemap(c, A, B):
    """Spacetime interplay: the second picture's brightness bends time inside the first
    picture — where B is dark, A runs live; where B lights up on its notes, A pulls back
    into its own past (one turn of the riff deep), with a subtle rim of B over it."""
    p = _lead(c)
    depth = max(0.45, min(2.2, (p.cell or 16) * c.six))
    return {"background": "#000000", "layers": [_act(A), _act(B, **{"as": "chronos", "depth": round(depth, 3), "gain": 3.5, "ground": True}), _act(B, blend="add", fade=0.14)], "filters": []}


@combo("stagepass")
def c_stagepass(c, A, B):
    """Two pictures sharing a 3D stage: they weave past each other in depth on the riff's
    turn so each occludes the other cleanly in turn as it sweeps into the foreground."""
    p = _lead(c)
    per = max(2, math.ceil(5.5 / ((p.cell or 16) * c.six)))
    u = f"({p.turn}/{per} + 0.125)"
    return {
        "background": "#000000",
        "layers": [{
            "type": "stage", "blend": "normal",
            "camera": {"x": 0, "y": 0, "z": -1.1, "zoom": 1.2, "roll": f"0.012*sin({u})", "fog": 0.08},
            "actors": [
                {"use": A, "name": "a", "mask": "rect", "res": 0.7, "x": f"0.72*sin({u})", "y": f"0.12*cos({u})", "z": f"0.8 + 0.5*cos({u})", "scale": 0.84},
                {"use": B, "name": "b", "mask": "rect", "res": 0.7, "x": "0 - actor.a.x", "y": "0 - actor.a.y", "z": "1.6 - actor.a.z", "scale": 0.84},
            ],
        }],
        "filters": [],
    }


@combo("cutout")
def c_cutout(c, A, B):
    """Whatever is lit in one picture is cut out of the other in black."""
    return {"background": "#000000", "layers": [_act(A), _act(B, **{"as": "shadow", "gain": 5, "ground": True}), _act(B, blend="add", fade=0.12)], "filters": []}


@combo("negmask")
def c_negmask(c, A, B):
    """Where the second picture is lit, the first turns to its negative: two worlds that
    invert one another on the beat."""
    return {"background": "#000000", "layers": [_act(A), _act(B, **{"as": "negative", "gain": 4.5, "ground": True}), _act(B, blend="add", fade=0.14)], "filters": []}


@combo("warpby")
def c_warpby(c, A, B):
    """The second picture's motion and colour physically displace the first picture beneath it,
    with a faint ghost of the driver laid over."""
    return {"background": "#000000", "layers": [_act(A), _act(B, **{"as": "displace", "bend": 0.16}), _act(B, blend="screen", fade=0.32)], "filters": []}


@combo("embossed")
def c_embossed(c, A, B):
    """The second picture is pressed into the first as a bas-relief, catching light on its
    slopes."""
    return {"background": "#000000", "layers": [_act(A), _act(B, **{"as": "shade", "gain": 3.5}), _act(B, blend="add", fade=0.15)], "filters": []}


@combo("prismby")
def c_prismby(c, A, B):
    """Dispersive crystal interplay: the second picture acts as cut crystal over the first,
    splitting the first picture's R, G and B along the second picture's moving contours."""
    return {"background": "#000000", "layers": [_act(A), _act(B, **{"as": "prism", "bend": 0.14}), _act(B, blend="add", fade=0.12)], "filters": []}


@combo("mirrorby")
def c_mirrorby(c, A, B):
    """Reflective mask interplay: wherever the second picture lights up on its notes, the
    first picture flips into its mirror symmetry with silver specular contours."""
    return {"background": "#000000", "layers": [_act(A), _act(B, **{"as": "mirror", "gain": 4.0, "ground": True}), _act(B, blend="add", fade=0.1)], "filters": []}


@combo("ringed")
def c_ringed(c, A, B):
    """One picture in the middle, and round it the other's turn in frames: a ring of small
    frames of the first picture taken one after another, clockwise, a whole number of its
    riff's turns to the ring, while the second plays in the middle. The first is read as
    a dial of its own riff; the second is the present it goes round."""
    p = _lead(c)
    across, step = _ring(p.cell or 16)
    gap, edge = 0.1, 0.004
    ring = {"background": "#000000", "layers": [_act(A)],
            "filters": [{"type": "filmclock", "across": across, "step": step, "gap": gap, "edge": edge, "glow": 1.3, "flash": 0.6, "color": c.ink}]}
    # (The second picture covers the hole in the ring and the hole's border, and stops short of the frames.)
    inner = 1 - 2 / across - (gap * 0.5 / across + edge) * 0.9
    return {"background": "#000000", "layers": [_act(ring), _act(B, scale=round(inner, 4), mask="rect", blend="normal")], "filters": []}


@combo("diagonal")
def c_diagonal(c, A, B):
    """Slanted stripes across the frame, alternating between the two pictures and sliding a
    stripe each time the riff comes round."""
    p = _lead(c)
    nn = p.cell if p.cell and 4 <= p.cell <= 12 else 7
    return _two(c, A, B, cut="diagonal", cut_n=nn, cut_at=_step(p))


@combo("diamond")
def c_diamond(c, A, B):
    """Concentric diamond rings from the centre, alternating between the two pictures and
    stepping outward with each turn of the riff."""
    p = _lead(c)
    return _two(c, A, B, cut="diamond", cut_n=(5, 7, 6, 8)[c.seed % 4], cut_at=_step(p))


@combo("spiralcut")
def c_spiralcut(c, A, B):
    """Twisted spiral arms radiating from the centre, alternating between the two pictures
    and rotating continuously on the lead riff's turn."""
    p = _lead(c)
    per = max(2, math.ceil(6.0 / ((p.cell or 16) * c.six)))
    return _two(c, A, B, cut="spiral", cut_n=(4, 6, 8, 6)[c.seed % 4], cut_at=f"{p.turn}/{per}")


@combo("hexcut")
def c_hexcut(c, A, B):
    """Interlocking hexagonal honeycomb cells alternating between the two pictures, sliding
    a cell across on each turn of the lead riff."""
    p = _lead(c)
    return _two(c, A, B, cut="hex", cut_n=(6, 8, 7, 10)[c.seed % 4], cut_at=_step(p))


TRIOS = {}


def trio(name):
    def deco(f):
        TRIOS[name] = f
        return f
    return deco


def _ink(look, color, gain=1.6):
    """The look printed in one ink on black."""
    import copy
    look = copy.deepcopy(look)
    look["filters"] = look.get("filters", []) + [{"type": "remap", "gain": gain, "palette": ["#000000", color]}]
    return look


@trio("separation")
def c_separation(c, A, B, C):
    """Three pictures printed one over another, one in red, one in green, one in blue: where
    all three are lit the print is white."""
    return {"background": "#000000", "layers": [_act(_ink(A, "#ff0000"), blend="normal"), _act(_ink(B, "#00ff00"), blend="add"), _act(_ink(C, "#0000ff"), blend="add")], "filters": []}


@trio("thirds")
def c_thirds(c, A, B, C):
    """Three pictures, a third of the frame each."""
    cut = dict(cut="strips", cut_n=3, cut_mod=3)
    return {"background": "#000000", "camera": FLAT,
            "layers": [_act(A, x=-1.185, blend="normal", cut_take=0, **cut), _act(B, blend="normal", cut_take=1, **cut), _act(C, x=1.185, blend="normal", cut_take=2, **cut),
                       box(-1.515, 0, -0.1, 0.012, 2.6, 0.01, **glow(c.ink, 1)), box(1.515, 0, -0.1, 0.012, 2.6, 0.01, **glow(c.ink, 1))], "filters": []}


@trio("russian")
def c_russian(c, A, B, C):
    """One picture, a second inside it, a third inside that."""
    layers = [_act(A, blend="normal")]
    for k, (L, col) in enumerate(((B, c.ink), (C, c.a)), 1):
        sc = 0.6 ** k
        layers.append(box(0, 0, -0.1 * k, 4.545 * sc + 0.035, 2.557 * sc + 0.035, 0.01, **glow(col, 1)))
        layers.append(_act(L, scale=sc, mask="rect", blend="normal"))
    return {"background": "#000000", "camera": FLAT, "layers": layers, "filters": []}


@trio("flags")
def c_flags(c, A, B, C):
    """Three pictures in three bands across the frame, which change places each time the riff comes round."""
    p = _lead(c)
    per = max(1, round(1.8 / c.six / (p.cell or 16)))
    at = f"floor({p.turn}/{per})"
    cut = dict(cut="bands", cut_n=3, cut_mod=3, cut_at=at)
    return {"background": "#000000", "layers": [_act(A, blend="normal", cut_take=0, **cut), _act(B, blend="normal", cut_take=1, **cut), _act(C, blend="normal", cut_take=2, **cut)], "filters": []}


@trio("stage3")
def c_stage3(c, A, B, C):
    """Three-voice 3D orbital stage: three distinct scenes circle each other in true depth
    with normal-blend occlusion, each pulsing into foreground on its own riff's cadence."""
    P = c.riffs[:3]
    while len(P) < 3:
        P.append(P[0])
    p0 = _lead(c)
    per = max(2, math.ceil(6.5 / ((p0.cell or 16) * c.six)))
    u = f"({p0.turn}/{per})"
    return {
        "background": "#000000",
        "layers": [{
            "type": "stage", "blend": "normal",
            "camera": {"x": f"0.12*sin({u})", "y": f"0.06*cos({u}/2)", "z": -1.15, "zoom": 1.28, "roll": f"0.01*sin({u})", "fog": 0.08},
            "actors": [
                {"use": A, "name": "a", "mask": "rect", "res": 0.6, "x": f"0.78*sin({u})", "y": f"0.12*sin({P[0].turn}/2)", "z": f"1.0 + 0.52*cos({u})", "scale": f"0.78 + 0.06*{P[0].hit}"},
                {"use": B, "name": "b", "mask": "rect", "res": 0.6, "x": f"0.78*sin({u} + 0.3333)", "y": f"0.12*sin({P[1].turn}/2)", "z": f"1.0 + 0.52*cos({u} + 0.3333)", "scale": f"0.78 + 0.06*{P[1].hit}"},
                {"use": C, "name": "c", "mask": "rect", "res": 0.6, "x": f"0.78*sin({u} + 0.6667)", "y": f"0.12*sin({P[2].turn}/2)", "z": f"1.0 + 0.52*cos({u} + 0.6667)", "scale": f"0.78 + 0.06*{P[2].hit}"},
            ],
        }],
        "filters": [],
    }


@combo("lighten")
def c_lighten(c, A, B):
    """Both pictures at once: at each point, whichever is the lighter."""
    return {"background": "#000000", "layers": [_act(A), _act(B, blend="max")], "filters": []}


@combo("difference")
def c_difference(c, A, B):
    """The two pictures taken from one another: where they agree there is nothing."""
    return {"background": "#000000", "layers": [_act(A), _act(B, blend="difference")], "filters": []}


@combo("corner")
def c_corner(c, A, B):
    """One picture whole and the other small in a corner; they change places half way."""
    cx, cy = ((1.16, -0.62), (-1.16, -0.62), (1.16, 0.62), (-1.16, 0.62))[c.seed % 4]
    h = f"step(0.5, {c.prog})"
    return {"background": "#000000", "layers": [_act(A, fade=f"1 - {h}"), _act(B, fade=h), _act(B, x=cx, y=cy, scale=0.3, mask="rect", fade=f"1 - {h}"), _act(A, x=cx, y=cy, scale=0.3, mask="rect", fade=h)], "filters": []}


# ───────────────────────── the first film's studies, as idioms ─────────────────────────

def _old(c, tracks):
    """Set studies.py's scene state from this context."""
    import studies as S
    S.HELD = {p.name: p.cell for p in c.riffs + c.every if p.cell}
    S.SIXTEENTH = c.six
    S.HOLD = 10 ** 6            # these scenes are short: the plate is not cut into details
    S.START, S.END = c.a16, c.b16
    S.ANCHOR = {p.name: p.anchor for p in c.riffs + c.every if p.cell}
    S.SHOTS = []
    return S


def _names(c, k, cond=lambda p: True):
    return [p.name for p in c.riffs if cond(p)][:k]


@idiom(needs=2, fam="plate", cost=2)
def wheels(c):
    S = _old(c, None)
    use = _names(c, 3)          # (three: four in a row are too small to read)
    return S.wheels(use, c.a, use[-1])


@idiom(needs=1, fam="plate")
def photofinish(c):
    S = _old(c, None)
    use = _names(c, 3)
    return S.finish_line(use, c.a, use[-1], subject=("runner", "horse")[c.variant % 2], meet=bool(c.odd))


@idiom(needs=2, fam="plate", cost=2, max_cell=32)
def gears(c):
    S = _old(c, None)
    fit = sorted((p for p in c.riffs if 3 <= p.cell <= 32), key=lambda p: p.cell)
    train = max(([p for p in fit[i:] if p.cell <= 4 * fit[i].cell][:3] for i in range(len(fit))), key=len, default=[])
    if len(train) < 2:
        raise ValueError("no train")
    use = [p.name for p in train]
    return S.gears(use, c.a, use[-1])


@idiom(needs=1, fam="plate", cost=2, max_cell=9)
def picket(c):
    S = _old(c, None)
    short = sorted((p for p in c.riffs if 3 <= p.cell <= 9 and p.cell not in (4, 8)), key=lambda p: p.cell)[:2]
    if not short:
        raise ValueError("no short odd riff")
    use = [p.name for p in short]
    return S.fence(use, c.a, use[-1], subject=("pacer", "horse")[c.variant % 2])


@idiom(needs=1, fam="plate", cost=2, max_cell=16)
def discs(c):
    S = _old(c, None)
    fit = sorted((p for p in c.riffs if 3 <= p.cell <= 16), key=lambda p: p.cell)
    if not fit:
        raise ValueError("no ring")
    use = [p.name for p in fit][:3 if all(p.cell <= 8 for p in fit[:3]) else 2]
    return S.discs(use, c.a, use[-1], subject=("runner", "horse")[c.variant % 2], cells={p.name: p.cell for p in c.riffs})


@idiom(needs=1, fam="plate", cost=2)
def bounce(c):
    S = _old(c, None)
    has = sorted(c.riffs, key=lambda p: p.cell)
    run = max(([p for p in has[i:] if p.cell <= 4 * has[i].cell][:4] for i in range(len(has))), key=len, default=[])
    if not run or run[-1].cell < 4:
        raise ValueError("no riff long enough for a bounce to be seen")      # (a riff of a sixteenth or two only skims the floor)
    use = [p.name for p in run]
    return S.balls(use, c.a, use[-1])


@idiom(needs=1, fam="plate", cost=2)
def pendulums(c):
    S = _old(c, None)
    use = _names(c, 5)
    return S.pendulums(use, c.a, use[-1])


@idiom(needs=1, fam="plate", cost=2)
def marey(c):
    S = _old(c, None)
    use = _names(c, 3)
    return S.walkers(use, c.a, use[-1], subject=("walker", "horse", "runner", "pacer")[c.variant % 4])


@idiom(needs=1, fam="plate", cost=2)
def muybridge(c):
    S = _old(c, None)
    use = _names(c, 4)
    return S.sheet(use, c.a, use[1] if len(use) > 1 else None, subject=("walker", "horse", "runner")[c.variant % 3])


@idiom(needs=2, fam="plate", cost=2, max_cell=24)
def lamp_knot(c):
    S = _old(c, None)
    knot, had = [], set()
    for p in sorted((p for p in c.riffs if 3 <= p.cell <= 24), key=lambda p: p.cell):
        if p.cell not in had:
            had.add(p.cell), knot.append(p)
    knot = knot[:3]
    if len(knot) < 2:
        raise ValueError("no knot")
    use = [p.name for p in knot]
    return S.loops(use, c.a, use[-1], cells=[p.cell for p in knot])


@idiom(needs=1, fam="plate", cost=3)
def daylight(c):
    S = _old(c, None)
    use = _names(c, 3)
    place = S.chase if c.variant % 2 else S.studio
    return place(use, c.a, use[-1], subject=("walker", "horse", "dancer", "runner")[c.variant % 4], bars=c.bars, start=c.a16 / 16)


@idiom(needs=0, tune=True, fam="plate", cost=2)
def flight(c):
    S = _old(c, None)
    fl = c.tunes[:3]
    if not fl:
        raise ValueError("no tune")
    use = [p.name for p in fl]
    rng = {p.name: (max((p.lo - 24) / 84 - 0.01, 0), min((p.hi - 24) / 84 + 0.01, 1)) for p in fl}
    return S.flight(use, c.a, use[0], ranges=rng)


PLATES = ("wheels", "photofinish", "picket", "discs", "bounce", "pendulums", "marey", "muybridge", "flight", "ridges", "sonar", "harmonograph")       # these hold a plate (or build one up): they are started before they are seen: started a bar early


# ───────────────────────── treatments: what the picture is seen through ─────────────────────────

TREAT = {}


LIFT = {"type": "color", "exposure": 1.35, "gamma": 1.7}
# Guises that do not darken or shrink what they are given (or that lift it themselves).
NO_LIFT = {"plain", "itself", "newsprint", "negative", "flood", "relief", "blueprint", "solar", "infra", "carried", "kaleido", "mirror", "riso", "etched"}


def treat(name, ok=lambda c, info: True):
    def deco(f):
        def lifted(c, look):
            """A picture that is dim as it stands (a room at night, things on black) has its
            shadows lifted before a guise that would take more light from it: a dark room
            on a ball, or falling into itself, was nearly nothing. Once, however many guises."""
            if name not in NO_LIFT and getattr(c, "idiom", None) in DIM and "layers" in look and LIFT not in look.get("filters", []):
                look = _pre(look, dict(LIFT))
            return f(c, look)
        TREAT[name] = (lifted, ok)
        return f
    return deco


def _pre(look, *filters):
    """Put filters before the look's bloom (or at the end)."""
    fs = look.setdefault("filters", [])
    at = next((i for i, f in enumerate(fs) if f.get("type") == "bloom"), len(fs))
    look["filters"] = fs[:at] + list(filters) + fs[at:]
    return look


def _lead(c):
    return (c.riffs or c.drums or c.parts)[0]


@treat("plain")
def t_plain(c, look):
    return look


KALEIDO_UP = -0.55      # the camera filter's y that puts the picture's middle 0.55 above the frame's

KALEIDO_OK = set("spiral sunflower stringart moire vortex epicycle harmonograph strange eclipse armillary radial cube fireflies pond chladni tiles table strings slack combs tally blinds loom orrery "
                 "sonar mondrian maypole carousel ferris helix anemone membrane shatter interference hive maze venn tartan colony treerings eye moirefield ripplebath".split())


@treat("kaleido", ok=lambda c, info: info["f"].__name__ in KALEIDO_OK and c.riffs)
def t_kaleido(c, look):
    """As many mirrors as the riff has sixteenths."""
    p = c.riffs[0]
    nn = p.cell if 3 <= p.cell <= 13 else 6
    # The mirrors show the wedge that begins at `rotate`: keep it about the upright, where things stand.
    # the picture is first made small and put up into that wedge, so the middle of it is what the mirrors pass round.
    return _pre(look, {"type": "camera", "zoom": 0.75, "y": KALEIDO_UP}, {"type": "kaleido", "n": nn, "rotate": f"0.25 - {0.25 / nn:.4f} + {0.12 / nn:.4f}*sin({p.turn}/4)", "zoom": 1.0})


# Two guises at once (dealt where the music is full): one that moves the picture, then one
# that changes what it is made of, then one that works on it in time.
STACK = {"falling": 0, "coiled": 0, "ball": 0, "kaleido": 0, "mirror": 0, "wall": 0, "planet": 0, "wound": 0, "tunnel": 0, "hole": 0, "warp": 0, "spin": 0, "roll": 0, "hyperbolic": 0, "standing": 0, "anamorph": 0, "conformal": 0,
         "dots": 1, "newsprint": 1, "engraved": 1, "hatched": 1, "onebit": 1, "drawn": 1, "blueprint": 1, "typed": 1, "duotone": 1, "poster": 1, "flood": 1, "solar": 1, "relief": 1, "fringe": 1,
         "leaded": 1, "infra": 1, "woven": 1, "screen": 0, "papercut": 1, "ridged": 1, "knitted": 1, "sampler": 1, "bricks": 1, "beaded": 1, "reeded": 1, "louvers": 0, "woodcut": 1, "riso": 1, "etched": 1, "cathedral": 1,
         "puzzle": 2, "itself": 1, "carried": 2, "delayed": 2, "tracking": 2, "smoked": 2, "dripping": 2, "torn": 2, "water": 2, "echo": 2, "stop": 2, "combed": 2, "blown": 2, "overgrown": 2, "scanfold": 2, "duochrono": 2, "metered": 2,
         "recoil": 2, "looped": 2, "boomerang": 2, "receding": 2, "filmclock": 2, "exposed": 2}

# The guises that work on a recording of the picture.
TIMED = ("recoil", "looped", "boomerang", "receding", "filmclock", "exposed")
# Pairs of guises that leave only texture, or flood white (feedback+grow saturates to pale wash).
STACK_BAD = ({(a_, b_) for a_ in ("tunnel", "wall", "wound", "kaleido", "falling", "coiled", "hyperbolic", "anamorph", "conformal", "screen") for b_ in ("blueprint", "drawn", "typed", "engraved", "hatched", "knitted", "sampler", "beaded", "ridged", "itself", "woodcut", "riso", "etched", "dots", "cathedral")}
             | {(a_, "blown") for a_ in ("newsprint", "riso", "etched", "negative")}
             | {("blown", a_) for a_ in ("newsprint", "riso", "etched", "negative")}
             | {("tunnel", "overgrown"), ("overgrown", "tunnel"), ("itself", "carried"), ("carried", "itself"),
                ("scanfold", "delayed"), ("delayed", "scanfold"), ("duochrono", "delayed"), ("delayed", "duochrono"),
                ("duochrono", "scanfold"), ("scanfold", "duochrono"), ("metered", "stop"), ("stop", "metered"),
                ("metered", "delayed"), ("delayed", "metered"), ("metered", "tracking"), ("tracking", "metered")}
             # (The ones that play a recording of the picture do not go on one already held or played late.)
             | {(a_, b_) for a_ in TIMED for b_ in ("stop", "metered", "delayed", "scanfold", "duochrono", "echo", "carried") + TIMED if a_ != b_}
             | {(b_, a_) for a_ in TIMED for b_ in ("stop", "metered", "delayed", "scanfold", "duochrono", "echo", "carried")}
             # (Small frames of a picture that is already small frames, or a print of them, is only texture; and a plate exposed over and over fills one that is already full.)
             | {(a_, "filmclock") for a_ in ("tunnel", "wall", "wound", "kaleido", "falling", "coiled", "hyperbolic", "anamorph", "conformal", "screen", "nest", "itself", "typed", "newsprint", "dots")}
             | {(a_, "exposed") for a_ in ("wall", "kaleido", "itself", "screen", "typed", "newsprint", "dots", "flood", "poster", "woodcut", "riso", "etched", "papercut", "cathedral", "onebit", "hatched", "engraved")}
             # (Frames within frames of a picture that is already frames within frames, or a print of them, is only texture.)
             | {(a_, "receding") for a_ in ("tunnel", "wall", "wound", "kaleido", "falling", "coiled", "hyperbolic", "anamorph", "conformal", "screen", "nest", "itself")})

# Pictures that stand to one side, or are a line of things: half of one is not a picture.
# Pictures that can be drawn twice and joined (flat, and filling the frame or centred, so that
# a break along the joins shows): for two parts playing one riff out of step. `STRONG`: the
# ones a break shows best in; a song's own canon is one of these.
CANON = set("riley vortex moire blinds hive interference vasarely mandala albers hourglass specimen spiral eye tiles kandinsky sundial moons zen dominoes breakout".split())
STRONG = ("riley", "vortex", "moire", "blinds", "hive", "interference", "vasarely", "albers", "mandala")
# Pictures that go one way across the frame, so that the same picture turned round and run by a
# part that plays backwards is seen to go both ways at once.
HANDS = ("riley", "blinds", "dominoes", "breakout", "kandinsky", "vortex", "moons", "interference", "spiral", "sundial", "vasarely", "mandala")
# Pictures that fill the frame with light (cutting their lights out of another picture leaves nothing),
# and pictures with broad lights (another picture shown only through thin lines would be nearly dark).
FULL = set("barcode braille courses riley vasarely kandinsky suprematist rothko albers mondrian vortex moire tartan hive tiles testcard thermal aurora marbling ink blots score zen sundial shadowplay "
           "interference maypole railway stairs henge turbines tide escalator grove skein swings skyline murmur wheat seesaw rink lava clockfield ripplebath".split())
BROAD = FULL | set("overtones septlock recount palindrome cobweb pinion spire quicken haul periods sizes ledger squares zipper total rabbits beats reels dice chladni specimen numerals eclipse moons eye globe cube crystal blinds doors golden venn colony mandala fruit splitflap leader kit keys musicbox abacus billiard fan cinema gallery hilbert worldlines mycelium".split())
# Thin pictures (a twentieth of the frame lit, or less, as measured on a proof), and the guises
# that leave less of a picture than there was: a thin picture does not take those.
THIN = set("breakout searchlights solkattu remainder rain seismo metro epicycle pond tally crystal candles strange teletype odometer loom inset slack discs hourglass metro flight photofinish bounce strobe picket bifurcate turtle armillary star combs fractal fireworks tetris tesla moons lighthouse lanterns kelvin "
           "searchlights pong constellation sonar treerings strings harmonograph contour letters mobile keys trampoline".split())
SHRINKS = set("ball woven tracking roll wound screen planet hole mirror water flood poster knitted sampler spin combed ridged".split())
# Pictures on a white ground: laid over another by its lights, the white would be all there is.
WHITE = set("braille barcode kandinsky suprematist mondrian score blots marbling ink sundial zen tape riley vasarely testcard thermal courses".split())
# Where an idiom is at its best: the dealer leans to it there.
WANTS = {"rabbits": lambda c: any(p.cell in (34, 55) for p in c.riffs),
         "beats": lambda c: c.full < 0.5}
# Pictures that take a good while to become anything: not for a scene under five and a half seconds.
LONG = set("turtle strange harmonograph tetris hanoi marbling ink rink galton".split())
# Idioms whose colours are their own (a flame is not magenta): no cast of colour for the riff's length.
TRUE = set("barcode braille dice candles courses shadowplay zen sundial kandinsky suprematist mondrian testcard thermal hanoi barber".split())
MIRROR_BAD = set("overtones septlock recount palindrome cobweb pinion spire quicken haul periods sizes ledger ringing squares zipper total rabbits dice barcode braille trampoline hailstone hanoi breakout duel seesaw rink lifts kit teletype constellation stairs letters turtle escalator crossing press dominoes hammers keys galley musicbox seismo contour splitflap solkattu lanterns rain mobile wires skein flight "
                 "marquee odometer numerals tape score".split())
# Pictures that are mostly light: a print of their lights is a blank sheet.
BRIGHT = set("barcode braille marbling ink shadowplay sundial zen kandinsky suprematist rothko riley maypole railway stairs henge turbines tide escalator grove skein swings skyline murmur wheat wires semaphore blots score tape mondrian thermal testcard aurora eclipse storm seesaw lava".split())
# Pictures that are nothing until notes come: not for a passage where few do.
FED = set("rolls zipper loom barcode braille marbling ink letters pond lanterns fountain fireworks blots constellation seismo contour teletype rain score storm galton coins snow lava tesla switchboard".split())
# Pictures that take time to become anything: not for a flash.
SLOW = set("overtones septlock recount palindrome cobweb pinion spire quicken haul periods sizes ledger ringing squares total rabbits beats dice barcode braille strobe crystal hourglass measure marbling ink hanoi zen sundial drill bifurcate teletype tetris remainder loom combs colony tally automaton galton strange letters fruit turtle harmonograph billiard rink snow lava switchboard star".split())


@treat("mirror", ok=lambda c, info: info["fam"] not in ("sign", "mirror") and info["f"].__name__ not in MIRROR_BAD)
def t_mirror(c, look):
    return _pre(look, {"type": "mirror", "axis": ("x", "y", "xy")[c.seed % 3]})


@treat("slices", ok=lambda c, info: info["fam"] not in ("sign", "plate", "lattice"))
def t_slices(c, look):
    """The frame in strips, each a sixteenth older than the last: a bar across the frame (or
    a riff, rings, spiral, wave or checker of time)."""
    p = _lead(c)
    nn = (p.cell or 16) if c.seed % 2 else 16
    nn = nn * (2 if nn < 9 else 1)
    kind = ("across", "round", "spiral", "clock", "wave", "checker")[c.seed % 6]
    turn = (0, 0.5, 0.25, 0, 0.125, 0.0)[c.seed % 6]
    return _pre(look, {"type": "timeslice", "depth": f"{nn * c.six:g}", "bands": nn, "turn": turn, "shape": kind, "amount": c.arr})


@treat("stop", ok=lambda c, info: info["fam"] not in ("plate", "trace"))
def t_stop(c, look):
    """Stop motion: the picture is retaken only on the riff's notes."""
    p = _lead(c)
    return _pre(look, {"type": "step", "on": f"track.{p.name}", "melt": 0.15})


@treat("metered", ok=lambda c, info: info["fam"] not in ("plate", "trace", "sign", "type", "sheet", "count") and len(_cast(c, 4)) >= 2)
def t_metered(c, look):
    """Stop motion in parts: the frame is cut in bands (or rings, or wedges) dealt round the
    parts, and each band is retaken only on its own part's notes. The picture keeps as many
    times at once as there are parts playing; its bands agree where the parts do."""
    P = _cast(c, 4)
    shape = ("bands", "rings", "bands", "wedges", "bands", "grid")[c.seed % 6]
    count = {"bands": len(P) * (3 if len(P) == 2 else 2), "rings": len(P) * 2, "wedges": len(P) * 3, "grid": 4 * len(P)}[shape]
    f = {"type": "polystep", "shape": shape, "count": count, "flash": 0.32, "decay": 0.14, "seam": 0.0035, "turn": (0, 0.25, 0.07, -0.07)[c.seed // 6 % 4]}
    for k, p in zip(("on", "on2", "on3", "on4"), P):
        f[k] = f"track.{p.name}"
    return _pre(look, f)


@treat("tunnel", ok=lambda c, info: info["fam"] not in ("plate", "room", "body", "travel", "sign") and info["f"].__name__ not in ("crystal",))
def t_tunnel(c, look):
    return _pre(look, {"type": "feedback", "zoom": 1.035, "rotate": 0.01, "decay": 0.86, "mode": "max"})


@treat("sheet", ok=lambda c, info: info["fam"] not in ("plate", "sign", "lattice") and c.riffs and c.riffs[0].cell <= 16)
def t_sheet(c, look):
    """The frame as a sheet of as many pictures as the riff has sixteenths, one taken on each."""
    p = c.riffs[0]
    nn = p.cell
    cols = next(k for k in (4, 3, 5, 2, 6, 7) if k * math.ceil(nn / k) - nn <= 1 and math.ceil(nn / k) <= 4)
    return _pre(look, {"type": "panels", "cols": cols, "rows": math.ceil(nn / cols), "count": nn, "every": 0.25, "gap": 0.012, "flash": 0.3, "fit": "fill", "border": c.bg})


@treat("halves", ok=lambda c, info: info["fam"] not in ("plate", "sign", "lattice") and c.riffs and c.riffs[0].cell and c.riffs[0].cell % 8 == 0 and 2 <= c.riffs[0].cell // 8 <= 6)
def t_halves(c, look):
    """The frame as a sheet of as many pictures as the riff has half bars, one taken each half
    bar: while the riff comes round, each place on the sheet shows the same thing every time."""
    nn = c.riffs[0].cell // 8
    cols = {2: 2, 3: 3, 4: 2, 5: 3, 6: 3}[nn]
    return _pre(look, {"type": "panels", "cols": cols, "rows": math.ceil(nn / cols), "count": nn, "every": 2, "gap": 0.014, "flash": 0.35, "fit": "fill", "border": c.bg})


@treat("blocks", ok=lambda c, info: info["fam"] not in ("sign", "lattice", "plate") and info["f"].__name__ in BROAD)
def t_blocks(c, look):
    """Sixteen blocks across: the picture counted in common time, sharp again on the bar."""
    return _pre(look, {"type": "pixelate", "size": f"0.003 + {2 * 16 / 9 / 16:g}*pow(1 - fract(time.bar/2), 6)"})


@treat("duotone", ok=lambda c, info: info["fam"] not in ("plate", "type"))
def t_duotone(c, look):
    return _pre(look, {"type": "color", "exposure": 1.45}, {"type": "posterize", "levels": 4}, {"type": "remap", "palette": [c.bg, c.b, c.a, c.ink], "amount": c.arr})


@treat("fringe", ok=lambda c, info: True)
def t_fringe(c, look):
    p = _lead(c)
    look.setdefault("filters", []).append({"type": "chroma", "amount": f"0.002 + 0.012*{p.hit}", "angle": f"{p.turn}/4"})
    return look


@treat("lines", ok=lambda c, info: info["fam"] not in ("sign",))
def t_lines(c, look):
    look.setdefault("filters", []).append({"type": "scanlines", "amount": f"0.45*{c.arr}", "count": 16 * 9, "speed": 0})
    return look


@treat("roll", ok=lambda c, info: info["fam"] not in ("sign", "plate"))
def t_roll(c, look):
    """The camera turns with the riff: a notch a turn."""
    p = _lead(c)
    nn = p.cell or 16
    look.setdefault("filters", []).append({"type": "camera", "zoom": 1.25, "rotate": f"(floor({p.turn}) + smooth(0.7, 1, fract({p.turn})))/{nn}"})
    return look


@treat("dots", ok=lambda c, info: info["fam"] not in ("sign", "lattice", "plate"))
def t_dots(c, look):
    """Printed as a wall of lamps, a bar of sixty-four across."""
    return _pre(look, {"type": "halftone", "count": 64, "angle": 0, "gain": 1.6, "amount": c.arr})


@treat("newsprint", ok=lambda c, info: info["fam"] not in ("sign", "plate") and info["f"].__name__ not in ("splitflap", "teletype"))
def t_newsprint(c, look):
    """Printed in the paper: dark dots on a pale ground."""
    look["filters"] = [f for f in look.get("filters", []) if f.get("type") != "bloom"] + ([{"type": "color", "exposure": 1.3, "gamma": 1.8}] if getattr(c, "idiom", None) in DIM and LIFT not in look.get("filters", []) else []) + [     # (a dim room's shadows are lifted first: it printed as an empty page)
                                                                                                  {"type": "invert", "amount": 1}, {"type": "halftone", "count": 110, "angle": 0.125, "gain": 1.0, "ink": "#16161a", "paper": "#e9e4d6"}]
    return look


@treat("engraved", ok=lambda c, info: info["fam"] not in ("sign", "plate"))
def t_engraved(c, look):
    """Cut in lines, heavier where it is lighter; the lines lean a notch each time the riff comes round."""
    p = _lead(c)
    return _pre(look, {"type": "halftone", "mode": "lines", "count": 120, "angle": f"floor({p.turn})/16", "gain": 1.5, "ink": c.ink, "amount": c.arr})


@treat("hatched", ok=lambda c, info: info["fam"] not in ("sign", "plate"))
def t_hatched(c, look):
    return _pre(look, {"type": "halftone", "mode": "hatch", "count": 100, "angle": 0.07, "gain": 1.6, "amount": c.arr})


@treat("onebit", ok=lambda c, info: info["fam"] not in ("sign", "plate"))
def t_onebit(c, look):
    """Two colours and nothing between."""
    look["filters"] = [f for f in look.get("filters", []) if f.get("type") != "bloom"] + [{"type": "halftone", "mode": "dither", "count": 213, "angle": 0, "gain": 1.5, "ink": c.a, "paper": c.bg, "amount": c.arr}]
    return look


@treat("drawn", ok=lambda c, info: info["fam"] not in ("sign", "plate", "trace", "curve"))
def t_drawn(c, look):
    """A line drawing of it."""
    return _pre(look, {"type": "outline", "gain": 8, "width": 0.004, "amount": c.arr}, {"type": "bold", "radius": 0.0025})


@treat("blueprint", ok=lambda c, info: info["fam"] not in ("sign", "plate", "trace", "curve"))
def t_blueprint(c, look):
    look["filters"] = [f for f in look.get("filters", []) if f.get("type") != "bloom"] + [{"type": "outline", "gain": 8, "width": 0.004, "color": "#e8f1ff", "paper": "#12356b", "amount": c.arr}]
    return look


@treat("echo", ok=lambda c, info: info["fam"] not in ("plate", "sign"))
def t_echo(c, look):
    """Each riff-turn's picture stays, fainter, under the next."""
    p = _lead(c)
    return _pre(look, {"type": "step", "on": f"track.{p.name}", "melt": 0.6, "live": 0.75})


@treat("spin", ok=lambda c, info: info["f"].__name__ in KALEIDO_OK)
def t_spin(c, look):
    """The frame goes round once in the scene."""
    look.setdefault("filters", []).append({"type": "camera", "zoom": 1.3, "rotate": c.prog})
    return look


@treat("warp", ok=lambda c, info: info["fam"] not in ("sign", "plate"))
def t_warp(c, look):
    """Seen through water that the riff's notes disturb."""
    p = _lead(c)
    return _pre(look, {"type": "warp", "amount": f"(0.006 + 0.03*{p.hit})*{c.arr}", "scale": 3, "speed": 0.3})


@treat("hole", ok=lambda c, info: info["fam"] not in ("sign", "plate"))
def t_hole(c, look):
    """A heavy thing goes across in front of the picture, once round for four turns of the riff, and bends it."""
    p = _lead(c)
    look.setdefault("filters", []).append({"type": "lens", "x": f"1.1*cos({p.turn}/4)", "y": f"0.55*sin({p.turn}/4)", "mass": 0.3})
    return look


@treat("typed", ok=lambda c, info: info["fam"] not in ("sign", "plate", "type") and info["f"].__name__ not in ("moirefield",))
def t_typed(c, look):
    """Set in type: each part of the picture is the letter as heavy as it is light."""
    return _pre(look, {"type": "halftone", "mode": "glyphs", "count": 96, "gain": 1.65, "amount": c.arr})


@treat("wall", ok=lambda c, info: info["fam"] not in ("sign", "plate", "lattice", "sheet"))
def t_wall(c, look):
    """A wall of copies, as many across as the riff has sixteenths (or half as many), every
    other one turned over so that they join; the wall moves on a copy each time the riff comes round."""
    p = _lead(c)
    nn = p.cell or 16
    cols = nn if nn <= 6 else nn // 2 if nn % 2 == 0 and nn <= 12 else 3 + c.seed % 3
    return _pre(look, {"type": "tile", "cols": cols, "flip": ("mirror", "brick", "turn", "mirror")[c.seed % 4], "x": f"floor({p.turn}) + smooth(0.75, 1, fract({p.turn}))", "amount": c.arr})


@treat("planet", ok=lambda c, info: info["fam"] not in ("sign", "plate", "orbit"))
def t_planet(c, look):
    """Wrapped round a circle: what went across goes round, once for so many turns of the riff."""
    p = _lead(c)
    return _pre(look, {"type": "polar", "inner": 0.1, "outer": 1.02, "repeat": 1 + c.seed % 2, "turn": f"{p.turn}/{(p.cell or 16)}", "amount": c.arr})


@treat("wound", ok=lambda c, info: info["fam"] not in ("sign", "plate"))
def t_wound(c, look):
    """Wound up about the middle and let go again, once for two turns of the riff."""
    p = _lead(c)
    return _pre(look, {"type": "twirl", "amount": f"0.45*sin({p.turn}/2)", "radius": 1.5})


@treat("solar", ok=lambda c, info: info["fam"] not in ("sign", "plate", "ground"))
def t_solar(c, look):
    """Solarised: the lights turn dark and keep a bright edge."""
    look["filters"] = look.get("filters", []) + [{"type": "solarize", "threshold": 0.45, "amount": c.arr}]
    return look


@treat("relief", ok=lambda c, info: info["fam"] not in ("sign", "plate"))
def t_relief(c, look):
    """Pressed into a surface and lit from one side; the light goes round a notch each time the riff does."""
    p = _lead(c)
    look["filters"] = [f for f in look.get("filters", []) if f.get("type") != "bloom"] + [{"type": "relief", "angle": f"0.375 + floor({p.turn})/{p.cell or 16}", "depth": 5, "width": 0.004, "color": 0.3,
                                                                                         "amount": c.arr}]
    return look


@treat("torn", ok=lambda c, info: info["fam"] not in ("sign", "plate"))
def t_torn(c, look):
    """Torn into sixteen bands that slip on the riff's notes and slide home."""
    p = _lead(c)
    look.setdefault("filters", []).append({"type": "tear", "on": f"track.{p.name}", "amount": 0.14, "bands": 16, "decay": 0.3})
    return look


@treat("falling", ok=lambda c, info: info["fam"] not in ("sign", "plate", "type"))
def t_falling(c, look):
    """The picture holds itself in its middle, and that holds it again: we fall in, one
    frame deeper for every turn (or two, or four) of the riff."""
    p = _lead(c)
    per = max(1, math.ceil(2.6 / ((p.cell or 16) * c.six)))
    look["filters"] = look.get("filters", []) + [{"type": "droste", "ratio": (3, 2.5, 4)[c.seed % 3], "zoom": f"{p.turn}/{per}", "amount": c.arr}]
    return look


@treat("coiled", ok=lambda c, info: info["f"].__name__ in KALEIDO_OK)
def t_coiled(c, look):
    """Wound into a spiral that holds itself, and turning inward with the riff."""
    p = _lead(c)
    per = max(1, math.ceil(3.2 / ((p.cell or 16) * c.six)))
    look["filters"] = look.get("filters", []) + [{"type": "droste", "shape": "round", "ratio": 4, "arms": (1, -1, 2)[c.seed % 3], "zoom": f"{p.turn}/{per}", "amount": c.arr}]
    return look


@treat("ball", ok=lambda c, info: info["fam"] not in ("sign", "plate", "type", "body") and info["f"].__name__ not in ("fountain", "fireworks", "snow", "rain", "fireflies"))
def t_ball(c, look):
    """Wrapped round a ball that turns once for every few turns of the riff."""
    p = _lead(c)
    per = max(2, math.ceil(7.0 / ((p.cell or 16) * c.six)))
    look["filters"] = look.get("filters", []) + [{"type": "orb", "radius": 0.93, "turn": f"{p.turn}/{per}", "wrap": 2, "tilt": 0.035, "shade": 0.4, "ground": 0.0, "amount": c.arr},
                                              {"type": "color", "exposure": 1.3}]
    return look


@treat("smoked", ok=lambda c, info: info["fam"] not in ("sign", "plate", "type"))
def t_smoked(c, look):
    """Every light smokes: it is carried off in eddies and fades as it goes."""
    return _pre(look, {"type": "flow", "speed": 0.22, "decay": 2.2, "scale": 2.5 + (c.seed % 3), "change": 0.3, "amount": c.arr})


@treat("dripping", ok=lambda c, info: info["fam"] not in ("sign", "plate", "type"))
def t_dripping(c, look):
    """The picture runs: every light is drawn out downward (or, every other time, upward like flame)."""
    return _pre(look, {"type": "flow", "field": ("fall", "rise")[c.seed % 2], "speed": 0.3, "decay": 1.6, "amount": c.arr})


@treat("tracking", ok=lambda c, info: info["fam"] not in ("sign", "plate"))
def t_tracking(c, look):
    """A worn tape: the colours out of register, lines across it, and the picture slips on
    the riff's notes."""
    p = _lead(c)
    look["filters"] = look.get("filters", []) + [{"type": "chroma", "amount": 0.007, "angle": 0}, {"type": "tear", "on": f"track.{p.name}", "amount": 0.05, "bands": 48, "decay": 0.18},
                                                 {"type": "scanlines", "amount": 0.3, "count": 200, "speed": 3}, {"type": "color", "saturation": 1.3, "contrast": 1.1}]
    return look


@treat("infra", ok=lambda c, info: info["fam"] not in ("sign", "plate", "type") and not info.get("paper"))
def t_infra(c, look):
    """As a heat camera sees it: the dark cold, the lights hot."""
    look["filters"] = look.get("filters", []) + [{"type": "blur", "radius": 0.006}, {"type": "remap", "gain": 1.3, "palette": ["#05051a", "#2a0a5e", "#8a1a6a", "#d93a2a", "#f59a1a", "#fff27a", "#ffffff"], "amount": c.arr}]
    return look


@treat("combed", ok=lambda c, info: info["fam"] not in ("sign", "plate", "type"))
def t_combed(c, look):
    """Combed: along every line the lights are put in order, further each time the riff's
    note sounds, and let go again."""
    p = _lead(c)
    look.setdefault("env", {})["comb"] = {"on": f"track.{p.name}", "attack": "20ms", "decay": "700ms"}
    return _pre(look, {"type": "sort", "lo": 0.07, "dir": ("right", "down", "left", "up")[c.seed % 4], "length": "0.04 + 0.96*env.comb", "amount": c.arr})


@treat("woven", ok=lambda c, info: info["f"].__name__ in BROAD and info["fam"] not in ("type",))
def t_woven(c, look):
    """Woven of its own strips, over one and under one: every note of the riff draws the
    strips along themselves, and they come back into register after it."""
    p = _lead(c)
    look.setdefault("env", {})["weft"] = {"on": f"track.{p.name}", "attack": "20ms", "decay": "500ms"}
    count = p.cell or 12
    while count < 8:
        count *= 2
    return _pre(look, {"type": "weave", "count": min(count, 24), "slip": "1.6*env.weft", "shade": 0.55, "gap": 0.1, "amount": c.arr})


@treat("screen", ok=lambda c, info: info["fam"] not in ("sign", "plate", "type", "trace"))
def t_screen(c, look):
    """On a folding screen with a leaf for each sixteenth of the riff: it folds up and is
    opened flat again once in every turn."""
    p = _lead(c)
    count = p.cell or 8
    while count < 6:
        count *= 2
    return _pre(look, {"type": "pleat", "count": min(count, 20), "fold": f"0.1 + 0.3*(1 - cos({p.turn}))" if p.cell else 0.4, "shade": 0.42, "amount": c.arr})


def _unbloomed(look):
    look["filters"] = [f for f in look.get("filters", []) if f.get("type") != "bloom"]
    return look


@treat("papercut", ok=lambda c, info: info["f"].__name__ in BROAD and info["fam"] not in ("sign", "plate", "type") and info["f"].__name__ != "albers")
def t_papercut(c, look):
    """Cut from sheets of coloured paper laid one on another, each casting a shadow; the
    light goes round once for every few turns of the riff, and the shadows with it."""
    p = _lead(c)
    per = max(2, math.ceil(8.0 / ((p.cell or 16) * c.six)))
    inks = ["#17141c", c.bg if _lum(c.bg) > 0.08 else "#2a2530", c.a, c.b, c.c, "#f6efe0"]
    look = _unbloomed(look)
    look["filters"] += [{"type": "blur", "radius": 0.004}, {"type": "papercut", "levels": 6, "depth": 0.022, "angle": f"0.375 + {p.turn}/{per}", "shade": 0.6, "gain": 1.5, "palette": inks, "amount": c.arr}]
    return look


@treat("ridged", ok=lambda c, info: info["fam"] not in ("sign", "plate", "type", "trace") and info["f"].__name__ not in (THIN | {"semaphore", "shadowplay", "henge"}))
def t_ridged(c, look):
    """Drawn as a range of ridges, one line for each sixteenth of the riff (several times
    over), each standing as high as the picture is light and hiding the ones behind; the
    notes heave it."""
    p = _lead(c)
    look.setdefault("env", {})["heave"] = {"on": f"track.{p.name}", "attack": "10ms", "decay": "450ms"}
    count = p.cell or 16
    while count < 40:
        count *= 2
    look = _unbloomed(look)
    look["filters"] += [{"type": "blur", "radius": 0.006}, {"type": "color", "brightness": 0.05}, {"type": "terrain", "count": min(count, 88), "height": "0.11 + 0.07*env.heave", "width": 0.0036, "gain": 1.6, "keep": 0.3, "amount": c.arr}]
    return look


@treat("reeded", ok=lambda c, info: info["fam"] not in ("sign", "plate", "type"))
def t_reeded(c, look):
    """Seen through fluted/reeded prism glass: parallel cylindrical lenses that refract and
    disperse the picture into chromatic ribs, gliding with the riff."""
    p = _lead(c)
    count = p.cell or 16
    while count < 10:
        count *= 2
    while count > 28:
        count = math.ceil(count / 2)
    angle = (0.0, 0.06, -0.06, 0.25)[c.seed % 4]
    return _pre(look, {"type": "prism", "count": count, "bend": f"(0.045 + 0.045*{p.hit})", "split": 0.45, "angle": angle, "phase": f"{p.turn}", "gloss": 0.24, "amount": c.arr})


@treat("louvers", ok=lambda c, info: info["fam"] not in ("sign", "plate", "type") and info["f"].__name__ in BROAD)
def t_louvers(c, look):
    """Rotating Venetian slats across the frame: a wave of slats tilts and opens wide
    again once for every two turns of the riff (staying open enough to read)."""
    p = _lead(c)
    count = p.cell or 12
    while count < 7:
        count *= 2
    while count > 18:
        count = math.ceil(count / 2)
    per = max(1, math.ceil(3.0 / ((p.cell or 16) * c.six)))
    return _pre(look, {"type": "louver", "count": count, "turn": f"0.11*sin({p.turn}/{per})", "twist": 0.07, "shade": 0.35, "angle": (0.0, 0.04, -0.04, 0.25)[c.seed % 4], "amount": c.arr})


@treat("hyperbolic", ok=lambda c, info: info["f"].__name__ in KALEIDO_OK and info["f"].__name__ in BROAD and info["f"].__name__ not in WHITE and not info.get("paper") and c.riffs)
def t_hyperbolic(c, look):
    """Projected onto a Poincare hyperbolic disc: mirrored copies pack infinitely toward
    the circular horizon, rotating and breathing radially with the riff."""
    p = _lead(c)
    order = p.cell if 4 <= (p.cell or 0) <= 10 else (5, 6, 7, 8)[c.seed % 4]
    per = max(2, math.ceil(6.0 / ((p.cell or 16) * c.six)))
    return _pre(look, {"type": "hyper", "order": order, "depth": 1.65, "turn": f"{p.turn}/{per * 2}", "zoom": f"0.6*{p.turn}/{per}", "rim": 0.4, "amount": c.arr})


@treat("standing", ok=lambda c, info: info["fam"] not in ("sign", "plate", "type"))
def t_standing(c, look):
    """Standing-wave optical shear: the picture ripples along oriented harmonic waves with
    chromatic crest splitting, surging on every note of the riff."""
    p = _lead(c)
    look.setdefault("env", {})["swv"] = {"on": f"track.{p.name}", "attack": "15ms", "decay": "450ms"}
    waves = (2.5, 3.5, 4.0, 5.0)[c.seed % 4]
    angle = (0.0, 0.125, 0.25, -0.125)[c.seed % 4]
    return _pre(look, {"type": "slitwave", "waves": waves, "amp": "0.025 + 0.075*env.swv", "phase": f"{p.turn}/2", "angle": angle, "split": 0.45, "amount": c.arr})


@treat("woodcut", ok=lambda c, info: info["f"].__name__ in BROAD and info["fam"] not in ("sign", "plate", "type") and info["f"].__name__ not in WHITE)
def t_woodcut(c, look):
    """Linocut / woodblock print: bold carved grooves that swell and part around the lights,
    leaning a notch each turn of the riff."""
    p = _lead(c)
    look = _unbloomed(look)
    look["filters"] += [{"type": "woodcut", "count": (34, 42, 48, 38)[c.seed % 4], "angle": f"0.05 + floor({p.turn})/24", "bend": f"0.32 + 0.28*{p.hit}", "gain": 1.12, "paper": "#121014", "amount": c.arr}]
    return look


@treat("riso", ok=lambda c, info: info["f"].__name__ in BROAD and info["fam"] not in ("sign", "plate", "type") and info["f"].__name__ not in WHITE and info["f"].__name__ not in ("doors", "tartan"))
def t_riso(c, look):
    """Two-plate risograph print on warm paper: spot-ink plates slip out of register on
    each hit of the riff and snap back into overprint."""
    p = _lead(c)
    look = _unbloomed(look)
    look["filters"] += [{"type": "riso", "misreg": f"0.012 + 0.028*{p.hit}", "angle": f"0.08 + {p.turn}/4", "grain": 0.24, "gain": 1.38, "ink_a": c.a, "ink_b": c.b, "paper": "#eee6d4", "amount": c.arr}]
    return look


@treat("anamorph", ok=lambda c, info: info["f"].__name__ in BROAD and info["fam"] not in ("sign", "plate", "type") and info["f"].__name__ not in WHITE and not info.get("paper") and c.riffs)
def t_anamorph(c, look):
    """Cylindrical mirror anamorphosis: a vertical chrome cylinder sits at the centre
    reflecting the picture while the surrounding panorama sweeps round it with the riff."""
    p = _lead(c)
    per = max(2, math.ceil(6.0 / ((p.cell or 16) * c.six)))
    return _pre(look, {"type": "anamorph", "radius": f"0.26 + 0.05*{p.hit}", "turn": f"{p.turn}/{per}", "pull": 1.4, "sheen": 0.38, "amount": c.arr})


@treat("scanfold", ok=lambda c, info: info["fam"] not in ("sign", "plate", "type") and c.riffs)
def t_scanfold(c, look):
    """Spatiotemporal wave slit-scan: recent frames are folded across space along a moving
    harmonic wave locked to the riff's period, with subtle RGB time-splitting."""
    p = _lead(c)
    depth = max(0.55, min(2.2, (p.cell or 16) * c.six))
    folds = (2.0, 3.0, 2.5, 4.0)[c.seed % 4]
    angle = (0.0, 0.125, 0.25, -0.125)[c.seed % 4]
    return _pre(look, {"type": "scanfold", "depth": round(depth, 3), "folds": folds, "phase": f"{p.turn}/2", "angle": angle, "split": 0.22, "amount": c.arr})


@treat("etched", ok=lambda c, info: info["f"].__name__ in BROAD and info["fam"] not in ("sign", "plate", "type") and info["f"].__name__ not in WHITE and info["f"].__name__ not in ("fruit", "dice", "reels", "turbines", "venn"))
def t_etched(c, look):
    """Copperplate cross-hatch engraving on warm ivory stock: three burin hatch angles bite
    progressively deeper into shadows, rotating subtly on each turn of the riff."""
    p = _lead(c)
    look = _unbloomed(look)
    look["filters"] += [{"type": "etched", "count": (44, 52, 60, 48)[c.seed % 4], "angle": f"0.08 + floor({p.turn})/32", "gain": 1.35, "ink": "#15141c", "paper": "#efe9d8", "tint": 0.42, "amount": c.arr}]
    return look


@treat("conformal", ok=lambda c, info: info["f"].__name__ in KALEIDO_OK and info["f"].__name__ in BROAD and c.riffs)
def t_conformal(c, look):
    """Conformal Möbius sphere map: straight geometry curves into sweeping orthogonal arcs
    around an orbiting pole locked to the lead riff's cycle."""
    p = _lead(c)
    per = max(2, math.ceil(6.5 / ((p.cell or 16) * c.six)))
    return _pre(look, {"type": "mobius", "pole": f"0.34 + 0.14*{p.hit}", "turn": f"{p.turn}/{per}", "twist": f"0 - {p.turn}/{per * 2}", "zoom": 1.12, "amount": c.arr})


@treat("duochrono", ok=lambda c, info: info["fam"] not in ("sign", "plate", "type") and c.riffs)
def t_duochrono(c, look):
    """Complementary temporal parallax: live motion glows warm gold against a delayed echo
    in cool cyan (half a turn behind), so stillness holds neutral colour while every hit
    and sweep splits chromatically through time."""
    p = _lead(c)
    delay = max(0.22, min(1.4, (p.cell or 16) * c.six * 0.5))
    return _pre(look, {"type": "duochrono", "delay": round(delay, 3), "gain": 1.15, "shift": f"{p.turn}/4", "amount": c.arr})


def _knocker(c):
    """The part whose notes knock another's picture: the sparsest other riff or drum that
    still plays at least once a bar (and not so often that the picture never catches up)."""
    lead = _lead(c)
    others = [q for q in list(c.riffs) + list(c.drums) if q.name != lead.name and 1 <= q.rate <= 4.5]
    return min(others, key=lambda q: (q.rate, q.name)) if others else None


@treat("recoil", ok=lambda c, info: info["fam"] not in ("sign", "plate", "type") and c.riffs and _knocker(c) is not None)
def t_recoil(c, look):
    """Knocked back in time: every note of another part throws the picture back most of a
    beat, and it runs to catch up, as a tape does (the bars showing while it runs). One
    part's notes are jolts in the other's time."""
    q = _knocker(c)
    look.setdefault("env", {})["knock"] = {"on": f"track.{q.name}", "attack": "0ms", "decay": "300ms"}
    # (Thrown back at once, held there a tenth of a second, and caught up by half a second.)
    return _pre(look, {"type": "replay", "delay": "0.9*(1 - smooth(0.1, 0.5, env.knock.age))", "hold": 1.5, "wear": 0.5})


@treat("looped", ok=lambda c, info: info["fam"] not in ("sign", "plate", "type") and c.riffs and 6 <= (_lead(c).cell or 16) <= 32)
def t_looped(c, look):
    """A beat repeat: the last quarter of each turn of the riff does not come; the piece
    before it is played four times over in its place (a roll), and the picture is back in
    time on the turn."""
    p = _lead(c)
    turn = (p.cell or 16) / 4                       # beats
    win = max(0.5, round(turn / 4 * 4) / 4)          # the last quarter of it, on the sixteenth
    loop = win / 4
    u = f"({p.ph}*{turn:g} - {turn - win:g})"       # beats into the window (negative before it)
    return _pre(look, {"type": "replay", "delay": f"step(0, {u})*{loop:g}*(floor(max({u}, 0)/{loop:g}) + 1)", "hold": round(win + 0.75, 2), "wear": 0.3})


@treat("boomerang", ok=lambda c, info: info["fam"] not in ("sign", "plate", "type") and c.riffs and 6 <= (_lead(c).cell or 16) <= 16 and (_lead(c).cell or 16) * c.six <= 2.0)
def t_boomerang(c, look):
    """Time there and back: the picture goes forward for the first half of each turn of the
    riff and backward for the second, so it is at the turn's beginning again as the next
    begins. The riff is heard once and seen as a palindrome."""
    p = _lead(c)
    turn = (p.cell or 16) / 4                       # beats
    u = f"({p.ph}*{turn:g} - {turn / 2:g})"         # beats past the middle of the turn
    return _pre(look, {"type": "replay", "delay": f"2*max({u}, 0)", "hold": round(turn + 0.5, 2), "wear": 0.22})


@treat("receding", ok=lambda c, info: info["f"].__name__ in BROAD and info["f"].__name__ not in WHITE and info["fam"] not in ("sign", "plate", "type") and c.riffs)
def t_receding(c, look):
    """The past goes away down a corridor: inside the picture is the picture as it was a
    little earlier, in a frame; inside that an earlier one; six deep. The frames are a
    fifth of a turn of the riff apart (for a long riff, a tenth), so the innermost is a
    whole turn behind and in step with the outermost: a canon in depth. The corridor
    leans as the riff goes round, and the frames light on its notes."""
    p = _lead(c)
    turn = (p.cell or 16) / 4                       # beats
    span = turn if turn <= 2.5 else turn / 2
    return _pre(look, {"type": "timetunnel", "levels": 6, "step": round(span / 5, 4), "ratio": 0.76, "x": f"0.55*sin({p.turn}/2)", "y": f"0.4*cos({p.turn}/2)",
                       "edge": 0.005, "glow": f"0.35 + 1.1*{p.hit}", "fade": 0.93, "color": c.ink, "amount": c.arr})


def _ring(cell):
    """For a riff of `cell` sixteenths: how many frames across the top of a ring of frames
    (it has four times that less four), and the beats from one frame to the next, so that
    the ring is a whole number of the riff's turns and, where it can be, a frame is a
    sixteenth."""
    for across in (5, 4, 6, 7, 3):
        n = 4 * across - 4
        if n % cell == 0 and n // cell <= 4:
            return across, 0.25                     # a frame a sixteenth, the ring some turns
        if cell % n == 0 and cell // n <= 4:
            return across, 0.25 * (cell // n)       # the ring one turn, a frame some sixteenths
    turns = 1 if cell >= 13 else 2 if cell >= 7 else 4
    return 5, round(cell / 4 * turns / 16, 5)        # sixteen frames to that many turns


@treat("filmclock", ok=lambda c, info: info["f"].__name__ in BROAD and info["fam"] not in ("sign", "plate", "type") and c.riffs and (_lead(c).cell or 16) >= 3)
def t_filmclock(c, look):
    """The picture's own dial: the picture now in the middle, and round the edge a ring of
    small frames taken one after another, clockwise, each kept until the taking comes
    round again. The ring is a whole number of the riff's turns, so a frame always shows
    the same place in the riff: what changes in it from one round to the next is what the
    other parts have done meanwhile."""
    p = _lead(c)
    across, step = _ring(p.cell or 16)
    return _pre(look, {"type": "filmclock", "across": across, "step": step, "gap": 0.1, "edge": 0.004, "glow": 1.3, "flash": 0.6, "color": c.ink, "amount": c.arr})


@treat("exposed", ok=lambda c, info: info["f"].__name__ not in FULL and info["f"].__name__ not in WHITE and info["fam"] not in ("sign", "plate", "type", "print") and c.riffs
       and 1.5 <= _lead(c).rate <= 12)
def t_exposed(c, look):
    """A plate exposed on every note of the riff (a chronophotograph): the last eight
    pictures taken lie under the picture now, the older the dimmer and the cooler. What
    moves leaves a pose to a note, so the riff is seen as spacing: close where its notes
    come fast, a gap where it rests."""
    p = _lead(c)
    q = _knocker(c)
    if q is not None and c.seed % 2:
        # (Every other time it is another part that takes the pictures: its notes are the
        # shutter, the riff is what is photographed.)
        return _pre(look, {"type": "exposures", "on": f"track.{q.name}", "count": 6, "fade": 0.8, "keep": 0.9, "color": c.dim, "amount": c.arr})
    return _pre(look, {"type": "exposures", "on": f"track.{p.name}", "count": 8, "fade": 0.84, "keep": 0.9, "color": c.dim, "amount": c.arr})


@treat("cathedral", ok=lambda c, info: info["f"].__name__ in BROAD and info["fam"] not in ("sign", "plate", "type") and info["f"].__name__ not in WHITE)
def t_cathedral(c, look):
    """Cathedral bevelled stained glass: organic jewel-toned Voronoi panes bound in dark
    lead cames with faceted internal bevel highlights that flare on the riff's hits."""
    p = _lead(c)
    count = (14, 18, 22, 16)[c.seed % 4]
    return _pre(look, {"type": "stained", "count": count, "lead": 0.075, "bevel": f"0.5 + 0.55*{p.hit}", "drift": 0.45, "amount": c.arr})


def _stitch(c, look, mode, count, **kw):
    look = _unbloomed(look)
    look["filters"] += [{"type": "color", "exposure": 1.25, "saturation": 1.2}, {"type": "stitch", "mode": mode, "count": count, "amount": c.arr, **kw}]
    return look


@treat("knitted", ok=lambda c, info: info["f"].__name__ in BROAD and info["fam"] not in ("sign", "plate", "type"))
def t_knitted(c, look):
    """Knitted: a stitch for every bit of the picture, four to a sixteenth of the bar across."""
    return _stitch(c, look, "knit", 64, ground=0.1)


@treat("sampler", ok=lambda c, info: info["f"].__name__ in BROAD and info["fam"] not in ("sign", "plate", "type"))
def t_sampler(c, look):
    """Cross-stitched on dark linen."""
    return _stitch(c, look, "cross", 72, ground=0.05, paper="#141210")


@treat("bricks", ok=lambda c, info: info["f"].__name__ in BROAD and info["fam"] not in ("sign", "plate", "type") and info["f"].__name__ not in ("score", "tape"))
def t_bricks(c, look):
    """Built of studded bricks, as many across as three bars have sixteenths."""
    return _stitch(c, look, "brick", 48, ground=1.0)


@treat("beaded", ok=lambda c, info: info["f"].__name__ in BROAD and info["fam"] not in ("sign", "plate", "type"))
def t_beaded(c, look):
    """Threaded as beads on a dark ground."""
    return _stitch(c, look, "bead", 56, ground=0.03)


def _grid(n, cap=40):
    """A sheet of about n pieces, wider than tall: (cols, rows), cols*rows a multiple of n if it can be."""
    best = None
    for total in range(n, cap + 1, n):
        for rows in range(1, 7):
            if total % rows == 0:
                cols = total // rows
                fit = abs(math.log((cols / rows) / (16 / 9))) + 0.25 * (total < 10) + 0.02 * abs(total - 18)
                if best is None or fit < best[0]:
                    best = (fit, cols, rows)
    return (best[1], best[2]) if best else (6, 3)


@treat("puzzle", ok=lambda c, info: info["fam"] not in ("sign", "plate"))
def t_puzzle(c, look):
    """Cut into pieces, one for each sixteenth of a few turns of the riff: they lie about
    loose and a piece is put in place on every sixteenth until the picture is whole; it
    stands a while, and is taken apart again."""
    p = _lead(c)
    cols, rows = _grid(p.cell or 16)
    total = cols * rows
    span = 2.2 * total / (p.cell or 16)       # turns of the riff for one building and taking apart
    ph = f"fract({p.turn}/{span:g})"
    placed = f"{total}*min(clamp({ph}*2.3, 0, 1), clamp((1 - {ph})*7, 0, 1))"
    order = ("rows", "spiral", "scatter", "columns")[c.seed % 4]
    return _pre(look, {"type": "pieces", "cols": cols, "rows": rows, "placed": placed, "spread": 0.34, "gap": 0.003, "dim": 0.5, "order": order, "amount": c.arr})


# (Not a picture on paper or bright sky/field: it is light all over, so its copies are all as light as one another and blow out.)
@treat("itself", ok=lambda c, info: info["f"].__name__ in BROAD and info["fam"] not in ("sign", "plate", "type") and info["f"].__name__ not in WHITE and info["f"].__name__ not in ("wheat", "skein", "grove", "murmur", "daylight", "aurora", "rink", "turbines", "zen", "sundial"))
def t_itself(c, look):
    """Made of small copies of itself, as many across as the riff has sixteenths: the same
    at two sizes. Each turn of the riff it comes in from the copies to the whole."""
    p = _lead(c)
    nn = p.cell or 16
    while nn > 16:
        nn = math.ceil(nn / 2)
    while nn < 7:
        nn *= 2
    look = _unbloomed(look)
    dim = getattr(c, "idiom", None) in DIM      # (a dim picture's shadows are lifted first: its copies were darker still)
    bright_ = getattr(c, "idiom", None) in BRIGHT
    look["filters"] += [{"type": "color", "exposure": 1.35, "gamma": 1.7} if dim and LIFT not in look["filters"] else {"type": "color", "exposure": 0.92 if bright_ else 1.15},
                        {"type": "mosaic", "count": nn, "gain": 1.8 if bright_ else 2.4, "floor": 0.22 if dim else 0.14, "tint": 0.72, "amount": f"({c.arr})*(1 - 0.85*pow(fract({p.turn}/2), 6))"}]
    return look


@treat("carried", ok=lambda c, info: info["fam"] not in ("sign", "plate", "type", "art") and info["f"].__name__ not in THIN and info["f"].__name__ not in WHITE)
def t_carried(c, look):
    """A clean picture only once every turn or two of the riff: between them the old
    picture is dragged along, block by block, by whatever moves in the new one."""
    p = _lead(c)
    beats = (p.cell or 16) / 4
    while beats < 3:
        beats *= 2
    while beats > 9:
        beats /= 2
    look["filters"] = look.get("filters", []) + [{"type": "mosh", "every": f"{beats:g}", "hold": 0.97, "block": 0.045, "reach": 1.4, "residue": 0.7, "amount": c.arr},
                                                 {"type": "color", "saturation": 1.2}]
    return look


@treat("delayed", ok=lambda c, info: info["fam"] not in ("sign", "plate"))
def t_delayed(c, look):
    """The colours arrive one after another: whatever moves leads red and trails blue."""
    look["filters"] = look.get("filters", []) + [{"type": "lag", "green": 0.11, "blue": 0.28, "amount": c.arr}, {"type": "color", "saturation": 1.25}]
    return look


@treat("blown", ok=lambda c, info: info["fam"] not in ("sign", "plate", "type"))
def t_blown(c, look):
    """In a wind that gusts with the riff's notes: every light has a tail."""
    p = _lead(c)
    look.setdefault("env", {})["gust"] = {"on": f"track.{p.name}", "attack": "30ms", "decay": "900ms"}
    return _pre(look, {"type": "wind", "length": "0.05 + 0.5*env.gust", "ragged": 0.7, "dir": ("right", "up", "left", "down")[c.seed % 4], "amount": c.arr})


@treat("leaded", ok=lambda c, info: info["fam"] not in ("sign", "plate", "type"))
def t_leaded(c, look):
    """In leaded glass, with as many panes across as the riff has sixteenths (twice or four
    times as many for a short riff)."""
    p = _lead(c)
    n_ = p.cell or 16
    while n_ < 14:
        n_ *= 2
    look["filters"] = look.get("filters", []) + [{"type": "color", "exposure": 1.5}, {"type": "glass", "count": min(n_, 48), "lead": 0.14, "drift": 1.5, "amount": c.arr}]
    return look


@treat("overgrown", ok=lambda c, info: info["fam"] not in ("sign", "plate", "type"))
def t_overgrown(c, look):
    """Overgrown: the picture's lights sow something that feeds and spreads from them."""
    habit = ((0.055, 0.062), (0.029, 0.057), (0.035, 0.065), (0.046, 0.063))[c.seed % 4]
    return _pre(look, {"type": "grow", "feed": habit[0], "kill": habit[1], "speed": 1200, "sow": 0.7, "size": 150, "amount": c.arr})


@treat("water", ok=lambda c, info: info["fam"] not in ("sign", "plate"))
def t_water(c, look):
    """Every note of the riff drops a stone into the picture."""
    p = _lead(c)
    return _pre(look, {"type": "ripple", "on": f"track.{p.name}", "amount": 0.05, "speed": 1.3, "width": 0.16, "decay": 1.4, "x": (-0.6, 0.5, 0, 0.9)[c.seed % 4], "y": (0.2, -0.3, 0, 0.4)[c.seed % 4]})


def _lum(hexcol):
    """How light a colour is, 0..1."""
    h = hexcol.lstrip("#")
    r, g_, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g_ + 0.0722 * b


@treat("poster", ok=lambda c, info: info["fam"] not in ("sign", "plate", "ground", "place") and info["f"].__name__ not in BRIGHT)
def t_poster(c, look):
    """A two-colour print: the ground is the song's colour, flat, and whatever was light is black on it."""
    # (On a dark ground black would not show: there the lights are printed pale.)
    inks = [c.a, "#141418", "#0c0c10"] if _lum(c.a) > 0.3 else [c.a, "#efe8d6", "#fffaf0"]
    look["filters"] = [f for f in look.get("filters", []) if f.get("type") != "bloom"] + [{"type": "remap", "gain": 1.8, "palette": inks, "amount": c.arr}]
    return look


@treat("flood", ok=lambda c, info: info["fam"] not in ("sign", "plate", "ground", "place") and info["f"].__name__ not in BRIGHT)
def t_flood(c, look):
    """The other print: a deep ground of the song's second colour, and whatever was light is cream on it."""
    # (On a pale ground cream would not show: there the lights are printed dark, as in the poster.)
    inks = [c.b, "#f3ecd8", "#fffaf0"] if _lum(c.b) < 0.55 else [c.b, "#2a2630", "#121016"]
    look["filters"] = [f for f in look.get("filters", []) if f.get("type") != "bloom"] + [{"type": "remap", "gain": 1.8, "palette": inks, "amount": c.arr}]
    return look


@treat("negative", ok=lambda c, info: info["paper"])
def t_negative(c, look):
    """Printed as a negative: dark figures on a pale ground."""
    look["filters"] = [f for f in look.get("filters", []) if f.get("type") != "bloom"] + [{"type": "invert", "amount": 1}, {"type": "color", "brightness": -0.06, "contrast": 0.92, "saturation": 0.85}]
    return look


ARRIVES = ("dots", "engraved", "hatched", "drawn", "typed", "onebit", "blueprint", "lines", "warp", "slices", "duotone", "wall", "planet", "solar", "relief", "poster", "flood", "combed", "blown", "leaded",
           "overgrown", "falling", "coiled", "ball", "smoked", "dripping", "infra", "woven", "screen", "delayed", "papercut", "ridged", "knitted", "sampler", "bricks", "beaded", "itself", "carried", "reeded", "louvers", "hyperbolic", "standing", "woodcut", "riso", "anamorph", "scanfold", "etched", "conformal", "duochrono", "cathedral", "receding", "filmclock", "exposed")

# Idioms drawn in hair lines and points, made bolder so that they read at any size: how far
# each thing in them is spread (a fraction of the frame's height).
BOLD = {"numerals": 0.004, "orrery": 0.004, "kelvin": 0.004, "galton": 0.004, "sonar": 0.004, "treerings": 0.003, "combs": 0.004, "pond": 0.003, "remainder": 0.004, "constellation": 0.004,
        "tally": 0.003, "bifurcate": 0.003, "clockshop": 0.003, "strange": 0.002, "epicycle": 0.003, "seismo": 0.003, "harmonograph": 0.003, "strings": 0.002, "solkattu": 0.003,
        "teletype": 0.003, "turtle": 0.004, "slack": 0.003, "table": 0.003, "letters": 0.003, "metro": 0.003, "spiral": 0.002, "stringart": 0.002, "kelvin": 0.004, "moons": 0.002, "radial": 0.002,
        "pong": 0.003, "contour": 0.003, "armillary": 0.003, "changes": 0.002, "loom": 0.002, "discs": 0.0035, "picket": 0.003}


# Guises that add to a picture (copies, echoes, mirrors) rather than print it.
FILLS = ("kaleido", "mirror", "wall", "planet", "tunnel", "echo", "slices", "fringe", "spin", "roll", "wound", "water", "torn", "hole", "lines", "warp", "solar", "blown", "overgrown", "combed", "falling", "ball", "smoked", "dripping", "tracking", "screen", "delayed", "puzzle", "reeded", "hyperbolic", "standing")


def bolder(name, look):
    r = BOLD.get(name)
    return _pre(look, {"type": "bold", "radius": r}) if r else look


# Filters that go by the picture's depth, and so must come before anything that moves it.
DEPTH = ("tonemap", "shadowmap", "ao", "shadow", "atmos", "fog", "dof", "reflect", "rays", "aa", "flare")


def rostrum(c, look, kind):
    """The camera over the picture does one thing in the scene: pushes in, pulls back, goes
    across, leans, or cuts in close where the riff comes round part way through."""
    lead = _lead(c)
    g = c.prog
    sx, sy = (1 if c.seed % 2 else -1), (1 if (c.seed // 2) % 2 else -1)
    cell = lead.cell or 16
    mid = (c.a16 + c.b16) / 2
    m = (lead.anchor + round((mid - lead.anchor) / cell) * cell) / 4          # the riff's turn nearest half way (beats)
    f = {"push": {"zoom": f"1 + 0.38*{g}"}, "pull": {"zoom": f"1.38 - 0.38*{g}"},
         "across": {"zoom": 1.3, "x": f"{0.4 * sx:g}*({g}*2 - 1)"}, "lean": {"zoom": 1.16, "rotate": f"{0.035 * sx:g}*({g}*2 - 1)"},
         "punch": {"zoom": f"1 + 0.75*step({m:g}, time.beat)", "x": f"{0.45 * sx:g}*step({m:g}, time.beat)", "y": f"{0.2 * sy:g}*step({m:g}, time.beat)"},
         "release": {"zoom": f"1.75 - 0.75*step({m:g}, time.beat)", "x": f"{0.45 * sx:g}*(1 - step({m:g}, time.beat))", "y": f"{0.2 * sy:g}*(1 - step({m:g}, time.beat))"},
         # In a step closer each time the riff comes round; rocking with it; going across on a slant.
         "step": {"zoom": f"1 + {min(0.14, 0.7 / max(1.0, (c.b16 - c.a16) / cell)):g}*floor((time.beat*4 - {c.a16:g})/{cell})"},
         "rock": {"zoom": 1.14, "rotate": f"{0.022 * sx:g}*sin({lead.turn}/2)"},
         "drift": {"zoom": 1.32, "x": f"{0.42 * sx:g}*({g}*2 - 1)", "y": f"{0.2 * sy:g}*({g}*2 - 1)"}}[kind]
    fs = look.setdefault("filters", [])
    at = max((i + 1 for i, x in enumerate(fs) if x.get("type") in DEPTH), default=0)
    look["filters"] = fs[:at] + [{"type": "camera", **f}] + fs[at:]
    return look


MOVES = ("push", "punch", "across", "pull", "release", "lean", "step", "rock", "drift")
# What the camera does goes by what the band does: in as it builds, back as it thins.
MOVES_FOR = {1: ("push", "punch", "step"), -1: ("pull", "release"), 0: ("across", "lean", "rock", "drift")}


# The stock a song is printed on, where it has one of its own: filters over the whole song.
STOCK = {
    5: [{"type": "color", "contrast": 1.12}],
    9: [{"type": "color", "saturation": 0.82, "contrast": 1.06}, {"type": "grain", "amount": 0.07}],
    13: [{"type": "color", "saturation": 0.78}, {"type": "vignette", "amount": 0.3}],
    14: [{"type": "scanlines", "amount": 0.1, "count": 240, "speed": 0}],
    16: [{"type": "chroma", "amount": 0.003, "angle": 0.08}],
}


def master(title, style=0):
    """Over every scene of a song: its name for the first bars (each song's in its own
    way), the stock it is printed on, and the print's grain."""
    bar = "time.bar"
    name = title.upper()
    words = name.split()
    cream = "#f2efe6"
    gone = f"(1 - smooth(2.6, 3.3, {bar}))"
    black = lambda y, op=1: {"type": "shape", "sides": 4, "rotate": 0.125, "radius": 2.6, "width": 0, "fill": 1, "color": "#000000", "blend": "normal", "x": 0, "y": y, "opacity": op}  # noqa: E731
    # (The veil comes down over the first half bar: a song that another passes into is
    # landed on at its first frame, and that frame is the picture, not the veil.)
    veil = black(0, f"0.6*smooth(0, 0.5, {bar})*(1 - smooth(2.0, 2.8, {bar}))")
    kind = style % 17
    n_ = len(name)
    w = min(0.2, 3.1 / n_)
    place = f"(inst.i - {(n_ - 1) / 2})*{w:g}"
    letter = lambda **kw: {"type": "text", "repeat": n_, "text": name, "pick": "inst.i", "size": w * 1.05, "align": "center", "width": 0.13, "skew": 0, "x": place, "y": -w * 0.5, "color": cream,  # noqa: E731
                           "blend": "normal", "opacity": gone, **kw}
    if kind == 8:
        # The letters come down like snow, each in its own time, and settle.
        t = f"clamp(({bar} - 0.2 - 1.3*hash(inst.i*3.7))*1.6, 0, 1)"
        label = [veil, letter(y=f"{-w * 0.5:g} + 1.25*pow(1 - {t}, 2)", x=f"{place} + 0.1*sin({bar}*0.7 + hash(inst.i*1.9))*(1 - {t})", opacity=f"{gone}*step(0.001, {t})")]
    elif kind == 9:
        # Entered like a line in a ledger, a letter a sixteenth, then ruled off twice.
        typed = f"step(inst.i + 1, ({bar} - 0.25)*16)"
        rule = lambda y, at: {"type": "shape", "repeat": 64, "sides": 4, "rotate": 0.125, "radius": 0.006, "width": 0, "fill": 1, "color": cream, "blend": "normal", "x": f"(inst.i + 0.5)*{w * n_ / 64:g} - {w * n_ / 2:g}", "y": y,  # noqa: E731
                              "opacity": f"{gone}*step(inst.i + 1, ({bar} - {at})*64)"}
        label = [veil, letter(opacity=f"{gone}*{typed}"),
                 {"type": "shape", "sides": 4, "rotate": 0.125, "radius": w * 0.45, "width": 0, "fill": 1, "color": cream, "blend": "normal", "x": f"(min(floor(({bar} - 0.25)*16), {n_}) - {(n_ - 1) / 2})*{w:g}", "y": 0,
                  "opacity": f"{gone}*step(0.25, {bar})*step(fract({bar}*8), 0.5)*step({bar}, 2.0)"},
                 rule(-w * 0.8, 1.6), rule(-w * 0.8 - 0.025, 1.9)]
    elif kind == 10:
        # It swings to on its hinge, over and back, and comes to rest.
        swing = f"(1.3*exp(0 - 1.6*{bar})*cos({bar}*1.25))"
        label = [veil, {"type": "text", "text": name, "size": 0.2, "x": -1.0, "y": -0.1, "align": "left", "color": cream, "width": 0.12, "skew": swing, "blend": "normal", "opacity": f"{gone}*smooth(0.1, 0.5, {bar})"},
                 {"type": "shape", "sides": 4, "rotate": 0.125, "radius": 0.006, "repeat": 3, "width": 0, "fill": 1, "color": cream, "blend": "normal", "x": -1.07, "y": "(inst.i - 1)*0.12", "opacity": f"{gone}*smooth(0.1, 0.5, {bar})"}]
    elif kind == 11:
        # Dealt out by two hands: every other letter from above, the rest from below.
        odd = "(inst.i - 2*floor(inst.i/2))"
        t = f"smooth(0, 1, ({bar} - 0.2)*8 - inst.i*0.5)"
        label = [veil, letter(y=f"{-w * 0.5:g} + (1 - 2*{odd})*0.9*(1 - {t})", palette=[cream, "#ffd9c2"], pos=f"{odd}*0.5", color=None, opacity=f"{gone}*step(0.001, {t})")]
        label[1].pop("color")
    elif kind == 12:
        # It is shown, and then it is somewhere else, and where it was a trace of it stays.
        move = f"smooth(1.2, 1.5, {bar})"
        label = [veil, {"type": "text", "text": name, "size": 0.15, "x": -0.35, "y": 0.12, "align": "center", "color": cream, "width": 0.12, "skew": 0, "blend": "normal", "opacity": f"{gone}*smooth(0.2, 0.5, {bar})*(1 - 0.78*{move})"},
                 {"type": "text", "text": name, "size": 0.15, "x": 0.35, "y": -0.3, "align": "center", "color": cream, "width": 0.12, "skew": 0, "blend": "normal", "opacity": f"{gone}*{move}"}]
    elif kind == 13:
        # A letter to a beat, and a stroke under each as it is counted.
        on = f"step(inst.i + 1, ({bar} - 0.2)*{max(4.0, n_ / 2.3):g})"
        label = [veil, letter(opacity=f"{gone}*{on}"),
                 {"type": "shape", "repeat": n_, "sides": 4, "rotate": 0.125, "radius": 0.02, "width": 0, "fill": 1, "color": cream, "blend": "normal", "x": place, "y": -w * 0.5 - 0.06, "opacity": f"0.8*{gone}*{on}"}]
    elif kind == 14:
        # Strung out right across the frame, and then the slack is taken up.
        taut = f"smooth(0.8, 2.0, {bar})"
        label = [veil, letter(x=f"(inst.i - {(n_ - 1) / 2})*mix({3.3 / n_:g}, {w:g}, {taut})", y=f"{-w * 0.5:g} - 0.25*(1 - {taut})*sin(inst.i/{2 * (n_ - 1)})", opacity=f"{gone}*smooth(0.1, 0.5, {bar})")]
    elif kind == 15:
        # Two printings that all but lie one over the other.
        off = f"(0.012 + 0.5*(1 - smooth(0.2, 2.0, {bar})))"
        both = lambda sgn, col: {"type": "text", "text": name, "size": 0.16, "x": f"{sgn}*{off}", "y": f"0 - 0.08 + {sgn}*0.3*{off}", "align": "center", "color": col, "width": 0.12, "skew": 0, "blend": "screen", "opacity": gone}  # noqa: E731
        label = [veil, both(-1, "#ff5a4f"), both(1, "#4fd8ff")]
    elif kind == 16:
        # A long way off, and coming on.
        near = f"smooth(0.1, 2.6, {bar})"
        label = [veil, {"type": "text", "text": name, "size": f"0.012 + 0.42*pow({near}, 2.2)", "x": 0, "y": f"0 - (0.012 + 0.42*pow({near}, 2.2))*0.5", "align": "center", "color": cream, "width": 0.12, "skew": 0, "blend": "normal",
                         "opacity": f"{gone}*smooth(0.05, 0.3, {bar})"}]
    elif kind == 0:
        # The picture is seen through a slit behind its name; then the slit opens.
        label = [black(f"0 - 2.03 - 1.9*smooth(2.4, 3.8, {bar})"), black(f"2.03 + 1.9*smooth(2.4, 3.8, {bar})"), veil,
                 {"type": "text", "text": name, "size": 0.17, "x": 0, "y": -0.07, "align": "center", "color": cream, "width": 0.12, "skew": 0, "blend": "normal",
                  "opacity": f"1 - smooth(2.4, 3.2, {bar})", "reveal": f"smooth(0.3, 1.6, {bar})"}]
    elif kind == 1:
        # Every letter turns over through the alphabet and falls into place, left to right.
        settled = f"step(inst.i + 1, ({bar} - 0.25)*{n_ / 1.6:g})"
        scr = f"floor(hash(floor(time.beat*4 + 0.01)*1.7 + inst.i*7.3)*26)"
        label = [veil, {"type": "text", "repeat": n_, "text": name + "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "pick": f"mix({n_} + {scr}, inst.i, {settled})", "size": w * 1.05, "align": "center", "width": 0.13, "skew": 0,
                        "x": f"(inst.i - {(n_ - 1) / 2})*{w:g}", "y": -w * 0.5, "color": cream, "blend": "normal", "opacity": f"{gone}*(0.5 + 0.5*{settled})"}]
    elif kind == 2:
        # A word at a time, as big as the frame, cut out of the picture.
        each = 2.6 / len(words)
        label = [{"type": "text", "text": wd, "size": min(0.62, 2.9 / (len(wd) * 0.72)), "x": 0, "y": -min(0.62, 2.9 / (len(wd) * 0.72)) * 0.45, "align": "center", "color": "#ffffff", "width": 0.2, "skew": 0, "blend": "difference",
                  "opacity": f"step({0.3 + k * each:g}, {bar})*step({bar}, {0.3 + (k + 1) * each:g})"} for k, wd in enumerate(words)]
    elif kind == 3:
        # Spaced out across the foot of the frame, a letter landing each sixteenth.
        n_ = len(name)
        label = [black(-2.32 - 1.2 * 0, f"0.75*{gone}") if False else {"type": "shape", "sides": 4, "rotate": 0.125, "radius": 2.6, "width": 0, "fill": 1, "color": "#000000", "blend": "normal", "x": 0, "y": -2.45,
                                                                      "opacity": f"0.8*{gone}"},
                 {"type": "text", "repeat": n_, "text": name, "pick": "inst.i", "size": 0.11, "align": "center", "width": 0.13, "skew": 0, "x": f"(inst.i - {(n_ - 1) / 2})*{3.2 / n_:g}",
                  "y": f"0 - 0.86 + 0.5*pow(1 - smooth(0, 0.25, {bar}*4 - 1.2 - inst.i*0.25), 2)", "color": cream, "blend": "normal", "opacity": f"{gone}*step(1.2 + inst.i*0.25, {bar}*4)"}]
    elif kind == 4:
        # Down the left-hand edge, a letter under a letter.
        n_ = len(name)
        h = min(0.2, 1.9 / n_)
        label = [{"type": "shape", "sides": 4, "rotate": 0.125, "radius": 2.6, "width": 0, "fill": 1, "color": "#000000", "blend": "normal", "x": -3.78, "y": 0, "opacity": f"0.9*{gone}"},
                 {"type": "text", "repeat": n_, "text": name, "pick": "inst.i", "size": h * 0.95, "align": "center", "width": 0.16, "skew": 0, "x": -1.56, "y": f"({(n_ - 1) / 2} - inst.i)*{h:g} - {h * 0.47:g}", "color": cream,
                  "blend": "normal", "opacity": f"{gone}*smooth(0, 0.3, {bar}*3 - 0.9 - inst.i*{2.4 / n_:g})"}]
    elif kind == 5:
        # Round a ring that turns once in the three bars.
        n_ = len(name) + 3
        a = f"(0.25 - inst.i/{n_} + {bar}/6)"
        label = [veil, {"type": "shape", "sides": 0, "radius": 0.5, "width": 0.004, "fill": 0, "color": cream, "opacity": f"0.6*{gone}"},
                 {"type": "text", "repeat": len(name), "text": name, "pick": "inst.i", "size": 0.13, "align": "center", "width": 0.13, "skew": 0, "x": f"0.66*cos({a})", "y": f"0.66*sin({a}) - 0.065", "color": cream,
                  "blend": "normal", "opacity": f"{gone}*smooth(0.2, 0.9, {bar})"}]
    elif kind == 6:
        # Written and then struck out, letter by letter.
        w_line = min(2.4, n_ * 0.115)
        label = [veil, {"type": "text", "text": name, "size": 0.15, "x": 0, "y": -0.07, "align": "center", "color": cream, "width": 0.12, "skew": 0.12, "blend": "normal", "opacity": gone, "reveal": f"smooth(0.3, 1.4, {bar})"},
                 {"type": "shape", "repeat": 72, "sides": 4, "rotate": 0.125, "radius": 0.017, "width": 0, "fill": 1, "color": cream, "blend": "normal",
                  "x": f"0 - {w_line / 2:g} + (inst.i + 0.5)*{w_line / 72:g}", "y": 0.005,
                  "opacity": f"{gone}*step(inst.i + 1, clamp(({bar} - 1.75)/0.85, 0, 1)*72)"}]
    else:
        # In the corner, small, with a rule that grows a sixteenth at a time across the frame.
        label = [{"type": "text", "text": name, "size": 0.12, "x": -1.62, "y": -0.83, "align": "left", "color": cream, "width": 0.15, "skew": 0, "blend": "normal", "opacity": gone, "reveal": f"smooth(0.2, 1.0, {bar})"},
                 {"type": "shape", "repeat": 48, "sides": 4, "rotate": 0.125, "radius": 0.012, "width": 0, "fill": 1, "color": cream, "blend": "normal", "x": "(inst.i + 0.5)*0.0675 - 1.62", "y": -0.9,
                  "opacity": f"{gone}*step(inst.i + 1, {bar}*16)"}]
    return {"layers": label, "filters": STOCK.get(style + 1, []) + [{"type": "grain", "amount": 0.04}, {"type": "vignette", "amount": 0.4}]}


for _n in ("sonar", "constellation", "seismo", "blots", "grove", "skein", "coins", "balance", "anemone"):
    REG[_n]["mood"] = -1
for _n in ("shatter", "gates", "highway", "mondrian"):
    REG[_n]["mood"] = 1

for _n in ("tape", "venn", "swings", "cradle", "aurora", "globe", "metro", "numerals"):
    REG[_n]["mood"] = -1
for _n in ("maze", "ropes", "galley", "storm", "crossing", "press", "zoetrope", "tartan"):
    REG[_n]["mood"] = 1

for _n in ("galton", "musicbox", "changes", "sympathy", "colony", "score"):
    REG[_n]["mood"] = -1
for _n in ("snow", "lava", "searchlights", "lifts", "switchboard", "rink"):
    REG[_n]["mood"] = -1
for _n in ("tesla", "duel", "trampoline", "billiard", "drill", "specimen"):
    REG[_n]["mood"] = 1
for _n in ("rothko", "albers", "kandinsky", "marbling", "ink", "hourglass", "sundial", "zen", "candles"):
    REG[_n]["mood"] = -1
for _n in ("breakout", "hanoi", "shadowplay", "strobe", "courses"):
    REG[_n]["mood"] = 1
for _n in ("barcode", "braille", "beats"):
    REG[_n]["mood"] = -1
for _n in ("reels", "dice"):
    REG[_n]["mood"] = 1
for _n in ("measure", "hailstone"):
    REG[_n]["mood"] = -1
for _n in ("riley", "vasarely", "suprematist"):
    REG[_n]["mood"] = 1
for _n in ("kit", "hive"):
    REG[_n]["mood"] = 1

for _n in ("teletype", "odometer", "treerings", "fractal", "letters"):
    REG[_n]["mood"] = -1
for _n in ("interference", "pong", "invaders", "eye"):
    REG[_n]["mood"] = 1

for _n in ("skyline", "murmur", "wheat", "leader", "splitflap"):
    REG[_n]["mood"] = -1
for _n in ("fruit", "tetris", "thermal", "testcard"):
    REG[_n]["mood"] = 1

# How heavy a passage each suits: calm ones for thin passages, loud ones for full ones.
for _n in ['pond', 'strings', 'wires', 'ridges', 'harmonograph', 'fireflies', 'mobile', 'contour', 'eclipse', 'orrery', 'tide', 'lighthouse', 'rain', 'spiral', 'sunflower', 'stairs', 'kelvin', 'table', 'armillary', 'choir', 'bifurcate', 'lanterns', 'slack', 'moons', 'fountain', 'golden', 'turtle', 'pendwave', 'flight']:
    REG[_n]["mood"] = -1
for _n in ['dominoes', 'radial', 'crystal', 'hammers', 'tiles', 'vortex', 'moire', 'railway', 'mandala', 'chorus', 'puppet', 'juggle', 'carousel', 'ferris', 'turbines', 'daylight', 'gears', 'membrane', 'strange', 'automaton', 'marquee', 'keys', 'quad', 'loom', 'helix', 'remainder', 'cube', 'fireworks', 'echoes', 'hands']:
    REG[_n]["mood"] = 1
