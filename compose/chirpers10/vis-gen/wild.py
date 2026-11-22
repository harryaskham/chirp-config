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
        """Turns of its riff since its anchor (unwrapped)."""
        return f"((time.beat*4 - {self.anchor:g})/{self.cell or 16})"

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
        layers.append(ball(f"{r}*cos({th})", "2.6 - 0.16*note.age", f"{r}*sin({th})", f"{0.085 - 0.012 * i:g}*(1 + 1.5*exp(0 - 4*note.age))", detail=6,
                           notes={"track": p.name, "past": 34}, **glow(c.col(i), "0.5 + 2.5*exp(0 - 2*note.age)")))
    # The column's hoops, a bar apart.
    layers.append({"type": "mesh", "shape": "torus", "detail": 40, "count": 8, "x": 0, "y": "2.6 - 0.64*(inst.i + fract(time.bar))", "z": 0, "scale": 1.75, "tube": 0.004, **glow(c.dim, 0.5)})
    return {"background": c.bg, "camera": cam("5.6*sin(time.bar/24)", 1.9, "0 - 5.6*cos(time.bar/24)", look=(0, 0.3, 0), zoom=1.25), "layers": layers, "filters": [bloom(c, 0.45, 0.02, 0.5)]}


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
    field = f"abs(mix({f(a, b)}, {f(a + 1, b + 2)}, {mixv}))"
    sand = f"(1 - smooth(0.0, 0.1 + 0.25*{A.hit}, {field}))"
    plate = box(0, 0, 0, 2.2, 2.2, 0.02, color="#0b0b0d", light=0.2, ambient=0.6, rim=0, paint_fine=True, paint_color=c.ink, paint=sand)
    return {"background": c.bg, "camera": cam(0, 0, -9, zoom=2.3, roll=f"0.01*sin(time.bar/8)"), "layers": [plate], "filters": [bloom(c, 0.3, 0.012)]}


@idiom(needs=2, fam="orbit")
def eclipse(c):
    """A sun, and a moon for each riff going over it once a turn. All of them cover it at once
    only where the riffs meet."""
    parts = c.riffs[:3]
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
    layers = [lamp(0, 3.0, 4.5, 2.6, "#ffe6b8", 16), lamp(-2, 5, -6, 0.25),
              floor(c, 0, "#18181c", 0.35), box(0, h, 5.5, 12, h + 0.6, 0.1, **glow("#ffdca0", 1.4))]
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
    for i, p in enumerate(P):
        y = (i - (len(P) - 1) / 2) * min(0.62, 4.2 / len(P))
        layers.append({"type": "beam", "from": [-4.1, y, 0], "to": [4.1, y, 0], "samples": 220, "width": 0.045, "glow": f"0.8 + 1.6*env.h{i}", "wave": f"0.3*env.h{i}", "waves": min(p.cell or 4, 14), "speed": 3,
                       "color": c.col(i)})
        for x in (-4.1, 4.1):
            layers.append(ball(x, y, 0, 0.05, 8, **glow(c.dim, 0.8)))
    return {"background": c.bg, "env": env, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.4, 0.02, 0.5)]}


@idiom(needs=1, fam="machine", cost=2)
def hammers(c):
    """A rank of hammers for each riff, one to a sixteenth of it that sounds; each lifts
    before its note and comes down on it."""
    parts = c.riffs[:3]
    layers = [lamp(-2, 5, -5, 1.3), floor(c, -0.12, "#17171a", 0.6)]
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
        hgt = 1.5 - 0.15 * i
        th = f"(0.75 - {p.turn})"
        layers.append({"type": "mesh", "shape": "cylinder", "detail": 12, "x": x, "y": hgt / 2, "z": z, "scale": 1, "sx": 0.14, "sy": hgt / 2, "sz": 0.14, **solid("#d8d4cc", 0.7)})
        layers.append(ball(x, hgt + 0.1, z, 0.13, 10, **glow(c.col(i), f"1.5 + 3*{p.hit}")))
        for sgn in (1, -1):
            layers.append({"type": "beam", "from": [x, hgt + 0.1, z], "to": [f"{x} + {sgn}*7*cos({th})", hgt + 0.1, f"{z} + {sgn}*7*sin({th})"], "width": 0.03, "taper": -7, "glow": 0.5, "fade": 0.9, "color": c.col(i), "samples": 60})
    return {"background": "#020308", "camera": cam("0.6*sin(time.bar/12)", 1.0, -6.5, look=(0, 1.0, 3), zoom=1.3), "layers": layers,
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
        layers.append(ball(x, y, 0, 0.085, 8, count=nn, **glow(c.col(i % len(c.riffs)), f"0.2 + 2.4*exp(0 - 1.4*{d})")))
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.5, 0.025, 0.5)]}


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
    layers = [{"type": "attractor", "kind": "logistic", "lo": 2.9, "hi": 4.0, "upto": f"2.95 + 1.06*{c.prog}", "points": 60000, "size": 1.5, "gain": "1.2 + 1.5*audio.low", "spread": 0.4, "palette": [c.ink, c.a, c.b]}]
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
    layers = [{"type": "attractor", "kind": kind, "a": f"{n(a)} + 0.06*sin({A.turn}/4)", "b": f"{n(b)} + 0.06*cos({B.turn}/4)", "c": f"{n(cc)} + 0.05*{A.hit}", "d": f"{n(d)} + 0.05*{B.hit}", "points": 70000, "size": 0.78,
               "gain": 1.4, "spread": 0.5, "rotate": "time.bar/32", "palette": [c.a, c.ink, c.b]}]
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
    layers = [lamp(-3, 5, -6, 1.6), lamp(4, -2, -5, 0.5, c.a), ball(0, 0, 0, 0.22, 14, **glow(c.b, 2))]
    for i, p in enumerate(parts):
        ax = ("rx", "rz", "rx", "rz")[i]
        layers.append({"type": "mesh", "shape": "torus", "detail": 56, "x": 0, "y": 0, "z": 0, "scale": 1.1 + 0.62 * i, "tube": 0.035 - 0.004 * i, ax: p.turn, "ry": 0.07 * i,
                       **solid(("#c9a45a", "#b9b3a6", "#c98a5a", "#8fa0b0")[i], 0.3, 0.95), "emit": f"0.25*{p.hit}"})
    return {"background": c.bg, "camera": cam("5.6*sin(time.bar/20)", 2.2, "0 - 5.6*cos(time.bar/20)", zoom=1.9), "layers": layers, "filters": post3d(-3, 5, -6, shadow=0.4)}


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
        layers.append({"type": "mesh", "shape": "torus", "detail": 40, "x": xs[i], "y": 1.3, "z": 0, "scale": (r + 0.14) / 0.8, "tube": 0.07, "rx": 0.25, **glow(c.dim, 1.0)})
        layers.append(ball(pins[i][0], pins[i][1], -0.05, 0.12, 8, **glow(c.col(i), f"1.2 + 1.5*{p.hit}")))
        layers.append({"type": "beam", "from": [xs[i], 1.3, 0], "to": [pins[i][0], pins[i][1], 0], "width": 0.01, "glow": 0.5, "color": c.dim})
    pts = [(f"{xs[0] - 1.3:g}", "1.3")] + pins + [(f"{pen_x:g}", pen_y)]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        layers.append({"type": "beam", "from": [x0, y0, -0.02], "to": [x1, y1, -0.02], "width": 0.022, "glow": 0.9, "color": c.ink, "samples": 30})
    layers.append({"type": "trail", "x": f"{pen_x:g} - 1.1*(var.nowb - time.beat)", "y": pen_y, "z": 0, "length": f"{6 * 0.5 / (c.bpm / 120):g}", "samples": 500, "width": 0.035, "taper": 0, "glow": 1.1, "fade": 0.5, "color": c.a})
    layers.append(ball(pen_x, pen_y, -0.05, 0.07, 8, **glow(c.a, 2.5)))
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
        layers.append(box(x, y, z, 0.03, h, 0.01, count=k, **glow(col, f"{emit} + 2*{near}")))
    row(1, 0, 0, 0.05, c.dim, 0.5)
    row(16, 0, 0, 0.22, c.dim, 0.7)
    row(A.cell, A.anchor, 0.75, 0.6, c.a, 0.6)
    row(B.cell, B.anchor, -0.75, 0.6, c.b, 0.6)
    # The round's own tooth: where both began together (or will).
    meet = next((s for s in range(L) if (s - A.anchor) % A.cell == 0 and (s - B.anchor) % B.cell == 0), None)
    if meet is not None:
        row(L, meet, 0, 1.6, c.ink, 0.9, z=-0.05)
    layers.append(box(0, 0, 0.1, 0.006, 2.4, 0.01, **glow(c.dim, 0.6)))
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.35, 0.016, 0.6)]}


@idiom(needs=2, fam="field3", cost=2)
def tiles(c):
    """A wall of tiles that turn over in waves: one wave runs across it as long as one riff,
    another down it as long as the other, and the pattern is their sum."""
    A, B = c.riffs[0], c.riffs[1]
    cols, rows = 32, 18
    ix, iy = f"(inst.i - {cols}*floor(inst.i/{cols}))", f"floor(inst.i/{cols})"
    a = f"(0.25*smooth(-0.3, 0.3, sin({A.turn} - {ix}/{A.cell}) + sin({B.turn} - {iy}/{B.cell})))"
    layers = [lamp(-3, 4, -7, 0.7), lamp(4, -1, -6, 0.5, c.a),
              box(f"({ix} - {(cols - 1) / 2})*0.285", f"({iy} - {(rows - 1) / 2})*0.285", 0, 0.13, 0.13, 0.012, count=cols * rows, ry=a, **solid("#8d8a84", 0.4, 0.6))]
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
    layers = [lamp(-2, 5, -6, 0.8), lamp(3, 0, -5, 0.5, c.a), box(0, 1.55, 0, 4.4, 0.07, 0.1, **solid("#3a2a1c", 0.8)),
              {"type": "mesh", "shape": "cone", "detail": 20, "count": nn, "x": f"{x} + 0.75*sin({sw})", "y": f"1.5 - 0.75*cos({sw})", "z": 0, "scale": sz * 1.25, "sy": 1.15, "rz": sw, **solid("#8a6a34", 0.4, 0.9),
               "emit": f"0.5*exp(0 - 0.9*{d})*{A.hit}"},
              {"type": "beam", "count": nn, "from": [x, 1.5, 0], "to": [f"{x} + 0.45*sin({sw})", f"1.5 - 0.45*cos({sw})", 0], "width": 0.012, "glow": 0.3, "color": c.dim}]
    return {"background": c.bg, "camera": cam("0.6*sin(time.bar/8)", 0.6, -7.5, look=(0, 0.75, 0), zoom=2.3), "layers": layers, "filters": post3d(-2, 5, -6, shadow=0.5)}


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
        layers.append({"type": "mesh", "shape": "sphere", "detail": 14, "x": fx, "y": y - 0.02, "z": fz, "scale": 0.5 - 0.08 * i, "sy": 0.08, "ry": f"0 - {th}", **solid(c.col(i), 0.5), "emit": f"0.25 + 0.5*{p.hit}"})
        px, py, pz = ex, y, ez
    layers.append({"type": "mesh", "shape": "sphere", "detail": 14, "x": px, "y": py - 0.4, "z": pz, "scale": 0.2, "sy": 0.08, **solid(c.ink, 0.5)})
    layers.append({"type": "beam", "from": [px, py, pz], "to": [px, py - 0.4, pz], "width": 0.008, "glow": 0.5, "color": c.dim})
    return {"background": c.bg, "camera": cam("1.2*sin(time.bar/9)", 2.6, -6, look=(0, 1.0, 0), zoom=1.6), "layers": layers,
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
        layers.append({"type": "beam", "from": [x, y, 0], "to": [nx, ny, 0], "width": 0.012, "glow": 0.6, "color": c.dim})
        layers.append({"type": "mesh", "shape": "torus", "detail": 48, "x": x, "y": y, "z": 0.05, "scale": Ls[i] / 0.8, "tube": 0.012 / Ls[i], "rx": 0.25, **glow(c.dim, 0.25)})
        x, y = nx, ny
    L = math.lcm(*[p.cell for p in P])
    layers.append({"type": "trail", "x": x, "y": y, "z": 0, "length": f"{min(L, 200) * 0.125 / (c.bpm / 120):g}", "samples": min(3000, max(300, L * 12)), "width": 0.012, "taper": 0, "glow": 1.0, "fade": 0.55, "color": c.a})
    layers.append(ball(x, y, -0.05, 0.06, 8, **glow(c.ink, 3)))
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
    layers = [floor(c, 0, "#0c0c10", 0.3), lamp(0, 3, -2, 0.8),
              {"type": "beam", "notes": N, "from": [w, y, z], "to": [wn, yn, zn], "width": 0.02, "glow": "1.2*exp(0 - 0.15*max(note.age, 0))", "color": c.a, "samples": 16},
              {"type": "beam", "notes": N, "from": [w, 0, z], "to": [w, y, z], "width": 0.008, "glow": 0.35, "color": c.dim, "samples": 8},
              ball(w, y, z, "0.07*(1 + 1.5*exp(0 - 3*max(note.age, 0)))", 8, notes=N, **glow(c.ink, "1 + 3*exp(0 - 3*max(note.age, 0))"))]
    return {"background": c.bg, "camera": cam(2.5, 1.9, -6.5, look=(-1.2, 1.2, 0), zoom=1.4), "layers": layers,
            "filters": [{"type": "reflect", "y": 0, "amount": 0.4}, {"type": "tonemap", "knee": 0.7}, {"type": "aa"}, bloom(c, 0.5, 0.02, 0.55)]}


@idiom(needs=0, fam="body", cost=3)
def choir(c):
    """A row of heads, one to a part: each opens its mouth as its part sounds."""
    P = (c.tunes + c.riffs + c.drums + c.parts)
    names, Q = set(), []
    for p in P:
        if p.name not in names:
            names.add(p.name), Q.append(p)
    Q = Q[:6]
    layers = [lamp(-2, 4, -6, 0.5), lamp(3, 2, -5, 0.5, c.a)]
    for i, p in enumerate(Q):
        x = (i - (len(Q) - 1) / 2) * 1.35
        layers.append({"type": "figure", "rig": "human", "motion": "sway", "energy": 0.4, "phase": i * 0.7, "x": x, "y": f"-1.75 + 0.05*track.{p.name}.level", "z": 0.3 * (i % 2), "scale": 2.0,
                       "mouth": f"clamp(1.6*track.{p.name}.level, 0, 1)", **skin(("#d9cdbb", "#c7b8a6")[i % 2], f"0.25*track.{p.name}.level"), "melt": 0.08,
                       "pose": {"arm_l": [0, 0, -0.02], "arm_r": [0, 0, 0.02], "head": [f"0 - 0.03 - 0.05*track.{p.name}.level", 0, 0]}})
    return {"background": c.bg, "camera": cam("0.6*sin(time.bar/10)", -0.3, -6.5, look=(0, -0.55, 0), zoom=2.0), "layers": layers, "filters": post3d(-2, 4, -6, shadow=0.4)}


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
    w = min(1.35, 8.4 / len(P))
    layers = []
    for i, p in enumerate(P):
        x = (i - (len(P) - 1) / 2) * w
        sag = f"(0.06 + 1.5*(1 - env.s{i}))"
        layers.append({"type": "beam", "from": [x - w * 0.42, 1.6, 0], "to": [x + w * 0.42, 1.6, 0], "width": 0.014, "glow": f"0.5 + 1.2*env.s{i}", "sag": sag, "color": c.col(i), "samples": 48})
        layers.append(box(x, f"1.6 - {sag} - 0.22", 0, 0.12, 0.2, 0.05, **glow(c.col(i), f"0.5 + 1.5*env.s{i}")))
        for sx in (-1, 1):
            layers.append(box(x + sx * w * 0.42, 1.7, 0.05, 0.02, 0.16, 0.02, **glow(c.dim, 0.7)))
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
    layers = [lamp(-2, 4, -6, 0.55), lamp(3, 1, -5, 0.4, c.a), floor(c, -1.9, "#16161a", 0.5)]
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
        layers.append({"type": "figure", "bones": bones, "motion": "none", "pose": pose, "x": x, "y": -1.8, "z": 0, "scale": 2.3, **skin(("#d8c7b4", "#c9b7a4")[i], f"0.15*{p.hit}"), "melt": 0.06})
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
        y = (len(P) - 1) * 1.15 - 2.3 * i
        w = min(1.0, 8.0 / nn)
        th = f"(0.75 - {p.turn})"
        layers.append({"type": "light", "x": f"4.6*cos({th})", "y": y, "z": f"4.6*sin({th})", "power": 1.6, "reach": 14 if len(P) == 1 else 8, "color": ("#fff4e0", c.a)[i]})
        d = f"(fract({p.turn} - inst.i/{nn})*{nn})"
        layers.append(ball(f"(inst.i - {(nn - 1) / 2})*{w:g}", y, 0, w * 0.4, 20, count=nn, **solid("#a7a39a", 0.95), emit=f"0.25*exp(0 - 1.5*{d})*{p.hit}"))
    return {"background": "#020204", "camera": FLAT, "layers": layers, "filters": [{"type": "tonemap", "knee": 0.75}, {"type": "aa"}, bloom(c, 0.3, 0.02, 0.8)]}


@idiom(needs=0, tune=True, fam="weather", cost=2)
def lanterns(c):
    """Every note of the tune is a lantern let go over the water, as far across as its
    pitch is high."""
    T = (c.tunes + c.riffs + c.parts)[0]
    x = f"({T.pitch(-3.6, 3.6)} + 0.25*sin(note.age/5 + note.beat/3))"
    layers = [{"type": "stars", "count": 500, "speed": 0, "size": 0.8, "light": 0.5, "twinkle": 0.3, "streak": 0},
              {"type": "mesh", "shape": "plane", "detail": 4, "x": 0, "y": -1.6, "z": 0, "scale": 30, "material": "pbr", "rough": 0.15, "metal": 0.3, "color": "#05080e", "rim": 0, "cull": True},
              box(x, "0 - 1.45 + 0.34*note.age", "0.2 + 2.2*hash(note.beat)", "0.3*(0.6 + note.vel)", "0.4*(0.6 + note.vel)", 0.3, notes={"track": T.name, "past": 16}, round=0.3,
                  **glow(c.a, "2.4*exp(0 - 0.07*note.age)*(0.8 + 0.2*noise(time.t*7 + note.beat))")),
              box(x, "0 - 1.45 + 0.34*note.age - 0.42*(0.6 + note.vel)", "0.2 + 2.2*hash(note.beat)", "0.1*(0.6 + note.vel)", 0.03, 0.1, notes={"track": T.name, "past": 16}, **glow("#fff2c8", "3*exp(0 - 0.07*note.age)"))]
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
        layers.append({"type": "particles", "on": f"track.{p.name}", "count": 40, "speed": f"1.7 + 0.9*track.{p.name}.vel", "spread": 0.045, "dir": 0.25, "life": 1.6, "gravity": 2.0, "drag": 0.1, "size": 0.009,
                       "x": x, "y": -0.8, "jitter": 0.012, "soft": 0.5, "hues": 0.05, "color": c.col(i), "shape": "spark"})
        layers.append({"type": "shape", "sides": 1, "radius": 0.02, "width": 0, "fill": 1, "color": c.col(i), "x": x, "y": -0.82, "glow": f"1 + 4*track.{p.name}.hit"})
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


@idiom(needs=1, fam="curve")
def turtle(c):
    """A lamp that walks straight and turns a corner each time a riff comes round, right for
    one riff and left for the other; the plate keeps its whole walk."""
    A = c.riffs[0]
    B = c.riffs[1] if len(c.riffs) > 1 else None
    t0 = math.floor((c.a16 - A.anchor) / A.cell)
    if not B:
        # One riff alone: the sides grow as it goes, so the walk winds outward (a square, a
        # three-cornered or a five-pointed winding, by turns).
        step, reach, g_ = ((0.25, 1.0, 0.22), (1 / 3, 0.8, 0.55), (0.4, 0.62, 0.5), (0.2, 1.0, 0.22), (1 / 6, 1.0, 0.22))[c.variant % 5]
        per = max(1, math.ceil((c.b16 - c.a16) / A.cell / 22))     # a corner every so many turns: no more than a score of corners
        turns = max(2.0, (c.b16 - c.a16) / (A.cell * per))
        k = f"floor(({A.turn} - {t0})/{per})"
        s0 = 3.6 * reach / (1 + g_ * turns)
        v = f"{s0:g}*(1 + {g_}*{k})/{A.cell * per * c.six:g}"
        h = f"{step:g}*{k}"
        thick = max(0.018, min(0.05, 0.3 * s0 * g_))
        return {"background": c.bg, "camera": FLAT,
                "vars": {"h": {"follow": h, "attack": "0ms", "release": "0ms"}, "px": {"integrate": f"{v}*cos(var.h)"}, "py": {"integrate": f"{v}*sin(var.h)"}},
                "layers": [ball("var.px", "var.py", 0, thick, 8, **glow(c.ink, 0.5)), ball("var.px", "var.py", -0.05, f"{thick:g} + 0.06*{A.hit}", 8, **glow(c.a, 1.2))],
                "filters": [{"type": "expose", "open": 1, "fade": 0, "live": 1, "mode": "light"}, bloom(c, 0.35, 0.016, 0.55)]}
    h = f"0.25*floor({A.turn})"
    if B:
        # Turn the second riff whichever way keeps the walk on the plate.
        r_opp = 1 / (1.57 * abs(1 - A.cell / B.cell)) if A.cell != B.cell else 99
        r_same = 1 / (1.57 * (1 + A.cell / B.cell))
        sgn = "-" if abs(r_opp - 1.4) < abs(r_same - 1.4) else "+"
        h = f"0.25*(floor({A.turn}) {sgn} floor({B.turn}))"
    turns = max(2.0, (c.b16 - c.a16) / A.cell)
    v = max(0.9, min(1.9, 11.0 / turns)) / (A.cell * c.six)     # a side: longer where there are few
    look = {"background": c.bg, "camera": FLAT,
            "vars": {"h": {"follow": h, "attack": "0ms", "release": "0ms"}, "px": {"integrate": f"{v:g}*cos(var.h)"}, "py": {"integrate": f"{v:g}*sin(var.h)"}},
            "layers": [ball("var.px", "var.py", 0, 0.09, 8, **glow(c.ink, 2.2)), ball("var.px", "var.py", -0.05, f"0.05 + 0.14*{A.hit}", 8, **glow(c.a, 3))],
            "filters": [{"type": "expose", "open": 1, "fade": 0, "live": 1, "mode": "light"}, bloom(c, 0.35, 0.016, 0.55)]}
    return look


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
        layers.append({"type": "mesh", "shape": "sphere", "detail": 9, "x": x, "y": 0.2, "z": 0, "scale": 0.72, "shatter": f"env.k{i}.age*step(env.k{i}.age, {max(0.2, (p.cell or 8) * c.six * 0.8):.2f}) - 0.001",
                       "burst": 1.6, "drop": 2.5, "tumble": 1.5, **solid(c.col(i), 0.15, 0.3), "emit": f"0.4*env.k{i}"})
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
    layers = [lamp(-2, 5, -6, 0.9), lamp(3, 2, -5, 0.5, c.c), floor(c, 0, "#17171b", 0.6)]
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
    layers = [lamp(-3, 6, -4, 1.2), lamp(3, 2, 4, 0.4, c.a),
              {"type": "mesh", "shape": "plane", "detail": 60, "x": 0, "y": 0, "z": 0, "scale": 30, "material": "pbr", "rough": 0.2, "metal": 0.2, "color": "#07141c", "rim": 0, "cull": True,
               "displace": "0.004*sin(vtx.x*9 + vtx.z*5 + time.t*0.4)"},
              box(0, 0.16, 0, 3.0, 0.16, 0.42, round=0.5, **solid("#5a3d26", 0.7)), box(0, 0.3, 0, 2.8, 0.03, 0.34, **solid("#2e2016", 0.9))]
    for p, side, col in ((A, -1, c.a), (B, 1, c.b)):
        nn = max(3, min(p.cell, 14))
        ph = f"({p.turn} - inst.i/{nn})"
        sweep = f"(0.06*sin({ph}))"
        dip = f"(0.035 + 0.03*cos({ph}))"
        x = f"((inst.i - {(nn - 1) / 2})*{5.2 / nn:g})"
        layers.append(box(x, 0.36, side * 1.25, 0.03, 0.03, 0.95, count=nn, ry=f"{side}*{sweep}", rx=f"{side}*{dip}", **solid("#c9b89a", 0.7), emit=f"0.3*exp(0 - 1.2*fract({ph})*{nn})"))
        layers.append(ball(x, 0.52, side * 0.3, 0.12, 8, count=nn, **solid(col, 0.6), emit=f"0.25 + 0.6*exp(0 - 1.2*fract({ph})*{nn})"))
    layers.append({"type": "motes", "mode": "drift", "count": 200, "w": 14, "h": 0.02, "d": 8, "y": 0.02, "z": 0, "fall": 0, "wind_x": -1.6, "wobble": 0, "size": 0.02, "stretch": 6, "glow": 0.5, "twinkle": 0, "color": "#9fd0e6"})
    look = {"background": "#04090d", "layers": layers, "filters": [{"type": "shadowmap", "amount": 0.5, "soft": 2, "size": 1024, "sun": 0, "x": -3, "y": 6, "z": -4}, {"type": "tonemap", "knee": 0.75}, {"type": "aa"}, bloom(c, 0.3, 0.016, 0.8)]}
    return shots(c, look, [cam(0.01, 8.5, -0.5, look=(0, 0, 0), zoom=1.7), cam(-5.5, 2.4, -4.5, look=(0, 0.3, 0), zoom=1.6), cam(6.5, 1.0, 0.01, look=(0, 0.4, 0), zoom=1.3)], A)


@idiom(needs=1, fam="swing", cost=2, max_cell=11)
def cradle(c):
    """A row of hanging balls, one to a sixteenth: the end ones go out in turn, and strike as
    the riff comes round and again half way."""
    P = [p for p in c.riffs if p.cell <= 11][:2]
    if not P:
        raise ValueError("too long")
    top, L, r = 3.0, 2.0, 0.21
    layers = [lamp(-3, 5, -6, 1.2), lamp(3, 1, -5, 0.5, c.a), floor(c, 0, "#131317", 0.3)]
    for i, p in enumerate(P):
        nn = max(3, p.cell)
        z = 1.6 * i
        x0 = (nn - 1) * r
        s = f"sin({p.turn})"
        thL, thR = f"(0 - 0.11*max({s}, 0))", f"(0.11*max(0 - {s}, 0))"
        layers.append(box(0, top, z, x0 + 0.5, 0.03, 0.03, **solid("#55595f", 0.4, 0.8)))
        layers.append(ball(f"(inst.i + 1 - {(nn - 1) / 2})*{2 * r}", top - L, z, r, 14, count=nn - 2, **solid(c.col(i), 0.2, 0.9), emit=f"0.15*{p.hit}"))
        layers.append(box(f"(inst.i + 1 - {(nn - 1) / 2})*{2 * r}", top - L / 2, z, 0.004, L / 2, 0.004, count=nn - 2, **glow(c.dim, 0.6)))
        for sx, th in ((-1, thL), (1, thR)):
            bx, by = f"({sx * x0} + {L}*sin({th}))", f"({top} - {L}*cos({th}))"
            layers.append(ball(bx, by, z, r, 14, **solid(c.col(i), 0.2, 0.9), emit=f"0.15*{p.hit}"))
            layers.append({"type": "beam", "from": [sx * x0, top, z], "to": [bx, by, z], "width": 0.008, "glow": 0.4, "color": c.dim, "samples": 4})
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
              {"type": "beam", "from": [x, 2.7, 0], "to": [f"{x} + 1.2*noise({cnt}*3.17)", -1.25, 0], "width": 0.06, "taper": 0.5, "glow": "5*env.k", "wave": 0.22, "waves": f"5 + 4*noise({cnt}*1.3)", "speed": 0, "color": "#e6ecff",
               "samples": 70},
              {"type": "beam", "from": [f"{x} + 0.3*noise({cnt}*3.17)", 1.2, 0], "to": [f"{x} + 1.6*noise({cnt}*5.9)", -0.3, 0], "width": 0.018, "taper": 0.8, "glow": "2.5*env.k", "wave": 0.15, "waves": 5, "speed": 0,
               "color": "#e6ecff", "samples": 40},
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
        hgt = f"(1.0 + 1.3*fbm(inst.i*0.05 + {j * 9}, time.t*0.12 + var.k*2, {j}))"
        layers.append(box(f"(inst.i - 60)*0.2 + 0.8*sin(time.t*0.02 + inst.i*0.004 + {j * 0.3})", f"0.9 + {hgt} + 0.6*sin(inst.i*0.011 + time.t*0.03 + {j * 0.2})", 3.0 + 2 * j, 0.1, hgt, 0.01, count=120,
                          **glow(col, f"0.25 + 0.3*{hgt} + 0.5*track.{T.name}.level"), opacity=0.5))
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
    layers = [lamp(0, 6, 0, 0.6), floor(c, 0, "#0c0c0f", 0.7), box(0, 0.01, 0, 12, 0.005, 0.5, **solid("#1d1d22", 0.9)), box(0, 0.011, 0, 0.5, 0.005, 12, **solid("#1d1d22", 0.9)),
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
    layers = [lamp(-3, 5, -6, 1.1), lamp(3, 2, -5, 0.5, c.a), floor(c, 0, "#121216", 0.6)]
    for i, p in enumerate(P):
        z = 1.7 * i
        layers.append(box(0, 0.35, z, 5.5, 0.05, 0.42, **solid("#2a2c33", 0.6, 0.5)))
        layers.append({"type": "mesh", "shape": "cylinder", "detail": 10, "count": 16, "x": "(inst.i - 7.5)*0.7", "y": 0.25, "z": z, "scale": 1, "sx": 0.09, "sy": 0.42, "sz": 0.09, "rx": 0.25, "ry": 0,
                       "rz": "time.beat*0.5", **solid("#55585f", 0.4, 0.8)})
        done = "step(0, note.age)"
        layers.append(box("0 - 1.5*note.age", f"0.4 + 0.17*(1 - 0.75*{done})", z, 0.17, f"0.17*(1 - 0.75*{done})", 0.17, notes={"track": p.name, "past": 4, "ahead": 4}, round=0.2,
                          **solid(c.col(i), 0.5), emit=f"0.2 + 1.2*exp(0 - 5*abs(note.age))"))
        layers.append(box(0, f"1.5 - 0.92*env.p{i}", z, 0.34, 0.4, 0.34, **solid("#8d9099", 0.3, 0.9)))
        layers.append(box(0, 2.3, z, 0.12, 0.6, 0.12, **solid("#55585f", 0.4, 0.8)))
        layers.append(box(0, 2.9, z, 0.7, 0.08, 0.5, **solid("#3a3d44", 0.5, 0.6)))
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
              {"type": "mesh", "shape": "sphere", "detail": 18, "mode": "wire", "x": 0, "y": 0, "z": 0, "scale": R, "ry": f"0 - {A.turn}", "color": c.ink, "emit": 1.1, "light": 0, "ambient": 0, "rim": 0, "width": 0.009},
              ball(0, 0, 0, R * 0.97, 24, **solid("#16233f", 0.8))]
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
    layers = [lamp(-3, 5, -6, 1.1), lamp(3, 2, -5, 0.5, c.a), floor(c, 0, "#16161a", 0.7), box(shove, 2.62, 0, 2.9, 0.05, 0.08, **wood)]
    for sx in (-1, 1):                                       # the chairs
        layers.append(box(sx * 2.6, 1.3, 0.25, 0.05, 1.3, 0.05, **wood))
        layers.append(box(sx * 2.6, 0.55, -0.15, 0.05, 0.55, 0.05, **wood))
        layers.append(box(sx * 2.6, 1.1, 0.05, 0.3, 0.04, 0.3, **wood))
        layers.append(box(sx * 2.6, 2.2, 0.25, 0.3, 0.25, 0.03, **wood))
    for i, (x, a) in enumerate(zip((-0.8, 0.8), th)):
        X = f"({shove} + {x})"
        layers.append(box(X, 2.15, 0, 0.3, 0.42, 0.12, **solid("#3a2a22", 0.6)))
        layers.append({"type": "mesh", "shape": "cylinder", "detail": 24, "x": X, "y": 2.2, "z": -0.13, "scale": 1, "sx": 0.22, "sy": 0.01, "sz": 0.22, "rx": 0.25, **solid("#e8e2d2", 0.5)})
        layers.append(box(f"{X} + 0.6*sin({a})", f"1.75 - 0.6*cos({a})", -0.05, 0.012, 0.6, 0.012, rz=a, **solid("#b8a468", 0.3, 0.9)))
        layers.append({"type": "mesh", "shape": "cylinder", "detail": 20, "x": f"{X} + 1.2*sin({a})", "y": f"1.75 - 1.2*cos({a})", "z": -0.06, "scale": 1, "sx": 0.16, "sy": 0.025, "sz": 0.16, "rx": 0.25,
                       **solid("#b8a468", 0.3, 0.9), "emit": f"0.5*exp(0 - 6*abs(sin({A.turn}{' + ' + off if i else ''})))"})
    return {"background": c.bg, "camera": cam("0.8*sin(time.bar/10)", 1.6, -7, look=(0, 1.5, 0), zoom=1.8), "layers": layers, "filters": post3d(-3, 5, -6, shadow=0.6)}


@idiom(needs=1, fam="grow")
def colony(c):
    """A dish: a new cell for every note, until there are as many as it can hold; after
    that one goes for each that comes."""
    A = c.riffs[0]
    cap = 144
    born = f"(time.beat*4 - {c.a16:g})*{max(0.5, min(3.0, cap / max((c.b16 - c.a16) * 0.6, 8))):g}"
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
    dr = min(0.16, 0.86 / (turns + 1))
    T = f"(time.beat*4 - {c.a16:g})/{A.cell}"
    layers = [{"type": "shape", "repeat": int(turns) + 2, "sides": 0, "radius": f"{dr:g}*(inst.i + 1)*(1 + 0.012*noise(inst.i*3.1))", "width": f"{dr * 0.22:g}", "fill": 0, "color": c.dim,
               "opacity": f"step(inst.i, {T})*(0.35 + 0.65*step({T} - 1, inst.i))"},
              {"type": "shape", "sides": 0, "radius": f"{dr:g}*({T} + 1)", "width": f"{dr * 0.3:g}", "fill": 0, "color": c.a},
              {"type": "shape", "notes": {"track": A.name, "past": turns * A.cell / 4 + 1}, "sides": 1, "radius": f"{dr * 0.3:g}*(0.6 + note.vel)*(1 + 1.5*exp(0 - 2*note.age))", "width": 0, "fill": 1, "color": c.ink,
               "x": f"{dr:g}*((note.beat*4 - {c.a16:g})/{A.cell} + 1)*sin({A.nph})", "y": f"{dr:g}*((note.beat*4 - {c.a16:g})/{A.cell} + 1)*cos({A.nph})", "opacity": f"step({c.a16 / 4:g}, note.beat)"}]
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
    layers.append({"type": "shape", "sides": 4, "rotate": 0.125, "radius": 0.03, "width": 0, "fill": 1, "color": c.a, "x": bx, "y": by, "glow": f"0.4 + 1.2*{A.hit}"})
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
    layers = [{"type": "shape", "repeat": W * H, "sides": 4, "rotate": 0.125, "radius": 0.06, "width": 0, "fill": 1, "x": X, "y": Y, "palette": [c.a, c.b, c.c], "pos": f"{row}/4"},
              {"type": "shape", "repeat": W * H, "sides": 4, "rotate": 0.125, "radius": 0.025, "width": 0, "fill": 1, "color": c.bg, "blend": "normal", "x": f"{X} - 0.02 + 0.04*{foot}", "y": f"{Y} + 0.012"},
              {"type": "shape", "repeat": W * H, "sides": 4, "rotate": 0.125, "radius": 0.02, "width": 0, "fill": 1, "x": f"{X} + (0.045 - 0.09*fract(inst.i/2)*2)*(0.5 + {foot})", "y": f"{Y} - 0.05",
               "palette": [c.a, c.b, c.c], "pos": f"{row}/4"}]
    for i, p in enumerate(P):
        nn = p.cell or 16
        layers.append({"type": "shape", "notes": {"track": p.name, "past": 3}, "sides": 4, "rotate": 0.125, "radius": 0.016, "width": 0, "fill": 1, "color": c.ink, "x": f"(({p.nstep} + 0.5)/{nn} - 0.5)*2.6",
                       "y": f"0 - 0.86 + 0.75*note.age", "opacity": "step(note.age, 2.3)", "glow": 0.5})
        layers.append({"type": "shape", "sides": 4, "rotate": 0.125, "radius": 0.05, "width": 0, "fill": 1, "color": c.col(i), "x": f"((floor(fract({p.turn})*{nn}) + 0.5)/{nn} - 0.5)*2.6", "y": -0.9 - 0.04 * i})
    return {"background": c.bg, "layers": layers, "filters": [bloom(c, 0.3, 0.014, 0.7)]}


# ───────────────────────── a ninth lot: places and grounds ─────────────────────────

@idiom(needs=1, fam="place", cost=2, max_cell=16)
def skyline(c):
    """A town at night: a tower for each riff, as many windows across as the riff has
    sixteenths and a floor for each time it comes round. Every note puts a light on."""
    P = c.riffs[:3]
    floors = 9
    layers = [{"type": "sky", "zenith": "#05060f", "horizon": "#1b2140", "ground": "#05060a", "sun": "#f4f1e6", "sun_yaw": 0.06, "sun_height": 0.2, "sun_size": 0.05, "clouds": 0},
              {"type": "stars", "count": 300, "size": 0.002, "twinkle": 0.4, "opacity": 0.7}, floor(c, 0, "#08090d", 0.4)]
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
                       "x": f"(inst.i - {(n_ - 1) / 2})*{w:g}", "y": y - w * 0.52, "color": c.ink, "opacity": f"0.8 + 0.2*{home}"})
        layers.append({"type": "shape", "repeat": n_, "sides": 4, "rotate": 0.125, "radius": w * 0.62, "width": 0, "fill": 1, "color": c.col(i), "blend": "add", "opacity": f"0.45*{home}",
                       "x": f"(inst.i - {(n_ - 1) / 2})*{w:g}", "y": y})
        layers.append({"type": "shape", "repeat": n_, "sides": 4, "rotate": 0.125, "radius": w * 0.62, "width": 0, "fill": 1, "color": c.bg, "blend": "normal", "x": f"(inst.i - {(n_ - 1) / 2})*{w:g}", "y": y, "scale": 1,
                       "opacity": 0} if False else
                      box(0, y * 2.557, -0.1, n_ * w * 2.557 / 2 + 0.1, 0.008, 0.01, **glow(c.bg, 1)))
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, 0.25, 0.012, 0.8)]}


@idiom(needs=2, fam="game", max_cell=24)
def fruit(c):
    """Three reels, each with as many pictures as its riff has sixteenths, each going a
    picture a sixteenth. They show three of a kind on the line only where the riffs meet."""
    P = c.riffs[:3]
    layers = []
    for i, p in enumerate(P):
        x = (i - (len(P) - 1) / 2) * 0.72
        nn = p.cell
        off = f"(fract((inst.i - floor(fract({p.turn})*{nn} + 0.01) - smooth(0.6, 1, fract(fract({p.turn})*{nn})))/{nn} + 0.5) - 0.5)*{nn}"
        kind = f"(inst.i - 5*floor(inst.i/5))"
        layers.append({"type": "shape", "sides": 4, "rotate": 0.125, "radius": 0.47, "width": 0, "fill": 1, "color": "#eeeae0", "blend": "normal", "x": x, "y": 0})
        layers.append({"type": "shape", "repeat": nn, "sides": f"3 + {kind}", "radius": f"0.15*step(abs({off}), 1.4)", "width": 0, "fill": 1, "x": x, "y": f"({off})*0.36", "blend": "normal",
                       "palette": [c.a, c.b, c.c, "#222226", c.a], "pos": f"{kind}/5", "star": f"0.5*step({kind}, 0.5)", "rotate": 0.25})
        layers.append({"type": "shape", "sides": 4, "rotate": 0.125, "radius": 0.5, "width": 0.012, "fill": 0, "color": c.dim, "x": x, "y": 0})
    for y in (-1, 1):
        layers.append({"type": "shape", "sides": 4, "rotate": 0.125, "radius": 2.4, "width": 0, "fill": 1, "color": c.bg, "blend": "normal", "x": 0, "y": y * (0.34 + 1.7)})
    meet = " * ".join(f"step(fract({p.turn})*{p.cell}, 1.0)" for p in P)
    layers.append({"type": "shape", "sides": 4, "rotate": 0.125, "radius": 1.2, "width": 0.01, "fill": 0, "color": c.ink, "x": 0, "y": 0, "opacity": 0})
    layers.append(box(0, 0, -0.2, 3.3, 0.012, 0.01, **glow(c.ink, f"0.6 + 4*{meet}")))
    return {"background": c.bg, "camera": FLAT, "layers": layers, "filters": [bloom(c, f"0.25 + 1.5*{meet}", 0.02, 0.75)]}


@idiom(needs=1, fam="game", max_cell=16)
def tetris(c):
    """A well as wide as the riff is long: every note drops a block into the column of its
    sixteenth, and each time the riff comes round a new row begins on top of the last."""
    P = c.riffs[:2]
    rows = 11
    layers = []
    for i, p in enumerate(P):
        nn = p.cell
        s_ = min(0.34, 3.6 / max(nn, sum(q.cell for q in P) / 1.0) * (1 if len(P) == 1 else 0.9))
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
    n1, big = _small(c, 0)
    n2, small = _small(c, 1 if len(c.riffs) > 1 else 0, skip=[n1])
    corner = ((1.16, -0.62), (-1.16, -0.62), (1.16, 0.62), (-1.16, 0.62))[c.seed % 4]
    layers = [{"type": "actor", "use": big, "x": 0, "y": 0, "scale": 1, "key": 0, "mask": "none"},
              {"type": "actor", "use": small, "x": corner[0], "y": corner[1], "scale": 0.3, "key": 0, "mask": "rect"}]
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
    layers = [{"type": "screen", "use": look, "x": 0, "y": 2.3, "z": 5, "w": 6.8, "h": 3.83, "glow": 2.6, "res": 360},
              box(0, 2.3, 5.1, 3.6, 2.1, 0.05, **solid("#16161a", 0.9)), lamp(0, 2.3, 3.0, 0.8, c.a, 8),
              {"type": "motes", "mode": "drift", "count": 200, "w": 4, "h": 2, "d": 8, "y": 2.8, "z": 0.5, "fall": 0.02, "wobble": 0.1, "size": 0.008, "glow": 0.4, "twinkle": 0.6, "color": "#cfd8ff"}]
    for row in range(2):
        nn = 8 - row
        layers.append({"type": "figure", "rig": "human", "motion": "none", "count": nn, "x": f"(inst.i - {(nn - 1) / 2})*0.95 + {0.45 * row}", "y": 0.55 - 0.25 * row, "z": 0.6 - 1.3 * row, "scale": 1.0, "ry": 0.5,
                       "color": "#020203", "light": 0.12, "ambient": 0.02, "rim": 0, "pose": {"head": [0, f"0.03*sin(time.bar/3 + inst.i*0.37)", 0]}})
    return {"background": "#020203", "camera": cam("0.3*sin(time.bar/12)", 1.6, -5.0, look=(0, 2.0, 5), zoom=2.2), "layers": layers, "filters": [{"type": "tonemap", "knee": 0.8}, {"type": "aa"}, bloom(c, 0.3, 0.02, 0.8)]}


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
    use = _names(c, 4)
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


PLATES = ("wheels", "photofinish", "picket", "discs", "bounce", "pendulums", "marey", "muybridge", "flight", "ridges", "turtle", "sonar", "harmonograph")       # these hold a plate (or build one up): they are started before they are seen: started a bar early


# ───────────────────────── treatments: what the picture is seen through ─────────────────────────

TREAT = {}


def treat(name, ok=lambda c, info: True):
    def deco(f):
        TREAT[name] = (f, ok)
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
                 "sonar mondrian maypole carousel ferris helix anemone membrane shatter interference hive maze venn tartan colony treerings eye".split())


@treat("kaleido", ok=lambda c, info: info["f"].__name__ in KALEIDO_OK and c.riffs)
def t_kaleido(c, look):
    """As many mirrors as the riff has sixteenths."""
    p = c.riffs[0]
    nn = p.cell if 3 <= p.cell <= 13 else 6
    # The mirrors show the wedge that begins at `rotate`: keep it about the upright, where things stand.
    # the picture is first made small and put up into that wedge, so the middle of it is what the mirrors pass round.
    return _pre(look, {"type": "camera", "zoom": 0.75, "y": KALEIDO_UP}, {"type": "kaleido", "n": nn, "rotate": f"0.25 - {0.25 / nn:.4f} + {0.12 / nn:.4f}*sin({p.turn}/4)", "zoom": 1.0})


# Pictures that stand to one side, or are a line of things: half of one is not a picture.
MIRROR_BAD = set("kit teletype constellation stairs letters turtle escalator crossing press dominoes hammers keys galley musicbox seismo contour splitflap solkattu lanterns rain mobile wires skein flight "
                 "marquee odometer numerals tape score".split())
# Pictures that are mostly light: a print of their lights is a blank sheet.
BRIGHT = set("maypole railway stairs henge turbines tide escalator grove skein swings skyline murmur wheat wires semaphore blots score tape mondrian thermal testcard aurora eclipse storm".split())
# Pictures that are nothing until notes come: not for a passage where few do.
FED = set("letters pond lanterns fountain fireworks blots constellation seismo contour teletype rain score storm galton coins".split())
# Pictures that take time to become anything: not for a flash.
SLOW = set("bifurcate teletype tetris remainder loom combs colony tally automaton galton strange letters fruit turtle harmonograph".split())


@treat("mirror", ok=lambda c, info: info["fam"] not in ("sign", "mirror") and info["f"].__name__ not in MIRROR_BAD)
def t_mirror(c, look):
    return _pre(look, {"type": "mirror", "axis": ("x", "y", "xy")[c.seed % 3]})


@treat("slices", ok=lambda c, info: info["fam"] not in ("sign", "plate", "lattice"))
def t_slices(c, look):
    """The frame in strips, each a sixteenth older than the last: a bar across the frame (or
    a riff, or rings out from the middle)."""
    p = _lead(c)
    nn = (p.cell or 16) if c.seed % 2 else 16
    nn = nn * (2 if nn < 9 else 1)
    kind = ("across", "round", "across", "clock")[c.seed % 4]
    return _pre(look, {"type": "timeslice", "depth": f"{nn * c.six:g}", "bands": nn, "turn": (0, 0.5, 0.25, 0)[c.seed % 4], "shape": kind, "amount": c.arr})


@treat("stop", ok=lambda c, info: info["fam"] not in ("plate", "trace"))
def t_stop(c, look):
    """Stop motion: the picture is retaken only on the riff's notes."""
    p = _lead(c)
    return _pre(look, {"type": "step", "on": f"track.{p.name}", "melt": 0.15})


@treat("tunnel", ok=lambda c, info: info["fam"] not in ("plate", "room", "body", "travel", "sign"))
def t_tunnel(c, look):
    return _pre(look, {"type": "feedback", "zoom": 1.035, "rotate": 0.01, "decay": 0.9, "mode": "max"})


@treat("sheet", ok=lambda c, info: info["fam"] not in ("plate", "sign", "lattice") and c.riffs and c.riffs[0].cell <= 16)
def t_sheet(c, look):
    """The frame as a sheet of as many pictures as the riff has sixteenths, one taken on each."""
    p = c.riffs[0]
    nn = p.cell
    cols = next(k for k in (4, 3, 5, 2, 6, 7) if k * math.ceil(nn / k) - nn <= 1 and math.ceil(nn / k) <= 4)
    return _pre(look, {"type": "panels", "cols": cols, "rows": math.ceil(nn / cols), "count": nn, "every": 0.25, "gap": 0.012, "flash": 0.3, "fit": "fill", "border": c.bg})


@treat("blocks", ok=lambda c, info: info["fam"] not in ("sign", "lattice", "plate"))
def t_blocks(c, look):
    """Sixteen blocks across: the picture counted in common time, sharp again on the bar."""
    return _pre(look, {"type": "pixelate", "size": f"0.003 + {2 * 16 / 9 / 16:g}*pow(1 - fract(time.bar/2), 6)"})


@treat("duotone", ok=lambda c, info: info["fam"] not in ("plate",))
def t_duotone(c, look):
    return _pre(look, {"type": "color", "exposure": 1.8}, {"type": "posterize", "levels": 4}, {"type": "remap", "palette": [c.bg, c.b, c.a, c.ink], "amount": c.arr})


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


@treat("newsprint", ok=lambda c, info: info["fam"] not in ("sign", "plate"))
def t_newsprint(c, look):
    """Printed in the paper: dark dots on a pale ground."""
    look["filters"] = [f for f in look.get("filters", []) if f.get("type") != "bloom"] + [{"type": "invert", "amount": 1}, {"type": "halftone", "count": 110, "angle": 0.125, "gain": 1.0, "ink": "#16161a", "paper": "#e9e4d6"}]
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


@treat("typed", ok=lambda c, info: info["fam"] not in ("sign", "plate", "type"))
def t_typed(c, look):
    """Set in type: each part of the picture is the letter as heavy as it is light."""
    return _pre(look, {"type": "halftone", "mode": "glyphs", "count": 96, "gain": 1.5, "amount": c.arr})


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


@treat("water", ok=lambda c, info: info["fam"] not in ("sign", "plate"))
def t_water(c, look):
    """Every note of the riff drops a stone into the picture."""
    p = _lead(c)
    return _pre(look, {"type": "ripple", "on": f"track.{p.name}", "amount": 0.05, "speed": 1.3, "width": 0.16, "decay": 1.4, "x": (-0.6, 0.5, 0, 0.9)[c.seed % 4], "y": (0.2, -0.3, 0, 0.4)[c.seed % 4]})


@treat("poster", ok=lambda c, info: info["fam"] not in ("sign", "plate", "ground", "place") and info["f"].__name__ not in BRIGHT)
def t_poster(c, look):
    """A two-colour print: the ground is the song's colour, flat, and whatever was light is black on it."""
    look["filters"] = [f for f in look.get("filters", []) if f.get("type") != "bloom"] + [{"type": "remap", "gain": 1.8, "palette": [c.a, "#141418", "#0c0c10"], "amount": c.arr}]
    return look


@treat("flood", ok=lambda c, info: info["fam"] not in ("sign", "plate", "ground", "place") and info["f"].__name__ not in BRIGHT)
def t_flood(c, look):
    """The other print: a deep ground of the song's second colour, and whatever was light is cream on it."""
    look["filters"] = [f for f in look.get("filters", []) if f.get("type") != "bloom"] + [{"type": "remap", "gain": 1.8, "palette": [c.b, "#f3ecd8", "#fffaf0"], "amount": c.arr}]
    return look


@treat("negative", ok=lambda c, info: info["paper"])
def t_negative(c, look):
    """Printed as a negative: dark figures on a pale ground."""
    look["filters"] = [f for f in look.get("filters", []) if f.get("type") != "bloom"] + [{"type": "invert", "amount": 1}, {"type": "color", "brightness": -0.06, "contrast": 0.92, "saturation": 0.85}]
    return look


ARRIVES = ("dots", "engraved", "hatched", "drawn", "typed", "onebit", "blueprint", "lines", "warp", "slices", "duotone", "wall", "planet", "solar", "relief", "poster", "flood")

# Idioms drawn in hair lines and points, made bolder so that they read at any size: how far
# each thing in them is spread (a fraction of the frame's height).
BOLD = {"numerals": 0.004, "orrery": 0.004, "kelvin": 0.004, "galton": 0.004, "sonar": 0.004, "treerings": 0.003, "combs": 0.004, "pond": 0.003, "remainder": 0.004, "constellation": 0.004,
        "tally": 0.003, "bifurcate": 0.003, "clockshop": 0.003, "strange": 0.002, "epicycle": 0.003, "seismo": 0.003, "harmonograph": 0.003, "strings": 0.002, "solkattu": 0.003,
        "teletype": 0.003, "turtle": 0.004, "slack": 0.003, "table": 0.003, "letters": 0.003, "metro": 0.003, "spiral": 0.002, "stringart": 0.002, "kelvin": 0.004, "moons": 0.002, "radial": 0.002,
        "pong": 0.003, "contour": 0.003, "armillary": 0.003, "changes": 0.002, "loom": 0.002}


# Guises that add to a picture (copies, echoes, mirrors) rather than print it.
FILLS = ("kaleido", "mirror", "wall", "planet", "tunnel", "echo", "slices", "fringe", "spin", "roll", "wound", "water", "torn", "hole", "lines", "warp", "solar")


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
         "release": {"zoom": f"1.75 - 0.75*step({m:g}, time.beat)", "x": f"{0.45 * sx:g}*(1 - step({m:g}, time.beat))", "y": f"{0.2 * sy:g}*(1 - step({m:g}, time.beat))"}}[kind]
    fs = look.setdefault("filters", [])
    at = max((i + 1 for i, x in enumerate(fs) if x.get("type") in DEPTH), default=0)
    look["filters"] = fs[:at] + [{"type": "camera", **f}] + fs[at:]
    return look


MOVES = ("push", "punch", "across", "pull", "release", "lean")


def master(title, style=0):
    """Over every scene of a song: its name for the first bars (each song's in its own
    way), and the print's grain."""
    bar = "time.bar"
    name = title.upper()
    words = name.split()
    cream = "#f2efe6"
    gone = f"(1 - smooth(2.6, 3.3, {bar}))"
    black = lambda y, op=1: {"type": "shape", "sides": 4, "rotate": 0.125, "radius": 2.6, "width": 0, "fill": 1, "color": "#000000", "blend": "normal", "x": 0, "y": y, "opacity": op}  # noqa: E731
    veil = black(0, f"0.6*(1 - smooth(2.0, 2.8, {bar}))")
    style %= 8
    if style == 0:
        # The picture is seen through a slit behind its name; then the slit opens.
        label = [black(f"0 - 2.03 - 1.9*smooth(2.4, 3.8, {bar})"), black(f"2.03 + 1.9*smooth(2.4, 3.8, {bar})"), veil,
                 {"type": "text", "text": name, "size": 0.17, "x": 0, "y": -0.07, "align": "center", "color": cream, "width": 0.12, "skew": 0, "blend": "normal",
                  "opacity": f"1 - smooth(2.4, 3.2, {bar})", "reveal": f"smooth(0.3, 1.6, {bar})"}]
    elif style == 1:
        # Every letter turns over through the alphabet and falls into place, left to right.
        n_ = len(name)
        w = min(0.2, 3.1 / n_)
        settled = f"step(inst.i + 1, ({bar} - 0.25)*{n_ / 1.6:g})"
        scr = f"floor(hash(floor(time.beat*4 + 0.01)*1.7 + inst.i*7.3)*26)"
        label = [veil, {"type": "text", "repeat": n_, "text": name + "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "pick": f"mix({n_} + {scr}, inst.i, {settled})", "size": w * 1.05, "align": "center", "width": 0.13, "skew": 0,
                        "x": f"(inst.i - {(n_ - 1) / 2})*{w:g}", "y": -w * 0.5, "color": cream, "blend": "normal", "opacity": f"{gone}*(0.5 + 0.5*{settled})"}]
    elif style == 2:
        # A word at a time, as big as the frame, cut out of the picture.
        each = 2.6 / len(words)
        label = [{"type": "text", "text": wd, "size": min(0.62, 2.9 / (len(wd) * 0.72)), "x": 0, "y": -min(0.62, 2.9 / (len(wd) * 0.72)) * 0.45, "align": "center", "color": "#ffffff", "width": 0.2, "skew": 0, "blend": "difference",
                  "opacity": f"step({0.3 + k * each:g}, {bar})*step({bar}, {0.3 + (k + 1) * each:g})"} for k, wd in enumerate(words)]
    elif style == 3:
        # Spaced out across the foot of the frame, a letter landing each sixteenth.
        n_ = len(name)
        label = [black(-2.32 - 1.2 * 0, f"0.75*{gone}") if False else {"type": "shape", "sides": 4, "rotate": 0.125, "radius": 2.6, "width": 0, "fill": 1, "color": "#000000", "blend": "normal", "x": 0, "y": -2.45,
                                                                      "opacity": f"0.8*{gone}"},
                 {"type": "text", "repeat": n_, "text": name, "pick": "inst.i", "size": 0.11, "align": "center", "width": 0.13, "skew": 0, "x": f"(inst.i - {(n_ - 1) / 2})*{3.2 / n_:g}",
                  "y": f"0 - 0.86 + 0.5*pow(1 - smooth(0, 0.25, {bar}*4 - 1.2 - inst.i*0.25), 2)", "color": cream, "blend": "normal", "opacity": f"{gone}*step(1.2 + inst.i*0.25, {bar}*4)"}]
    elif style == 4:
        # Down the left-hand edge, a letter under a letter.
        n_ = len(name)
        h = min(0.2, 1.9 / n_)
        label = [{"type": "shape", "sides": 4, "rotate": 0.125, "radius": 2.6, "width": 0, "fill": 1, "color": "#000000", "blend": "normal", "x": -3.78, "y": 0, "opacity": f"0.9*{gone}"},
                 {"type": "text", "repeat": n_, "text": name, "pick": "inst.i", "size": h * 0.95, "align": "center", "width": 0.16, "skew": 0, "x": -1.56, "y": f"({(n_ - 1) / 2} - inst.i)*{h:g} - {h * 0.47:g}", "color": cream,
                  "blend": "normal", "opacity": f"{gone}*smooth(0, 0.3, {bar}*3 - 0.9 - inst.i*{2.4 / n_:g})"}]
    elif style == 5:
        # Round a ring that turns once in the three bars.
        n_ = len(name) + 3
        a = f"(0.25 - inst.i/{n_} + {bar}/6)"
        label = [veil, {"type": "shape", "sides": 0, "radius": 0.5, "width": 0.004, "fill": 0, "color": cream, "opacity": f"0.6*{gone}"},
                 {"type": "text", "repeat": len(name), "text": name, "pick": "inst.i", "size": 0.13, "align": "center", "width": 0.13, "skew": 0, "x": f"0.66*cos({a})", "y": f"0.66*sin({a}) - 0.065", "color": cream,
                  "blend": "normal", "opacity": f"{gone}*smooth(0.2, 0.9, {bar})"}]
    elif style == 6:
        # Written and then struck out, letter by letter.
        label = [veil, {"type": "text", "text": name, "size": 0.15, "x": 0, "y": -0.07, "align": "center", "color": cream, "width": 0.12, "skew": 0.12, "blend": "normal", "opacity": gone, "reveal": f"smooth(0.3, 1.4, {bar})"},
                 {"type": "shape", "sides": 4, "rotate": 0.125, "radius": 1.0, "width": 0, "fill": 1, "color": cream, "blend": "normal", "x": f"0 - 2.9 + 1.5*smooth(2.0, 2.7, {bar})", "y": -1.41 + 0.005, "opacity": 0}]
    else:
        # In the corner, small, with a rule that grows a sixteenth at a time across the frame.
        label = [{"type": "text", "text": name, "size": 0.12, "x": -1.62, "y": -0.83, "align": "left", "color": cream, "width": 0.15, "skew": 0, "blend": "normal", "opacity": gone, "reveal": f"smooth(0.2, 1.0, {bar})"},
                 {"type": "shape", "repeat": 48, "sides": 4, "rotate": 0.125, "radius": 0.012, "width": 0, "fill": 1, "color": cream, "blend": "normal", "x": "(inst.i + 0.5)*0.0675 - 1.62", "y": -0.9,
                  "opacity": f"{gone}*step(inst.i + 1, {bar}*16)"}]
    return {"layers": label, "filters": [{"type": "grain", "amount": 0.04}, {"type": "vignette", "amount": 0.4}]}


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
