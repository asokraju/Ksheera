"""Simple, bright vector pictures for the kindergarten books.

Every icon is drawn by ICONS[name](c, x, y, s): centered at (x, y), fitting in an s × s box.
Words: the CVC picture words (cat, dog, bus, ...). Extras: vowel pictures (apple, egg, igloo, octopus,
umbrella) and theme pictures (train, car, solar panel, bulb, toolbox, mouse).
"""
import math

from reportlab.lib import colors

INK = colors.HexColor("#2b2b2b")
WHT = colors.white
YEL, ORG, RED = colors.HexColor("#FFD23F"), colors.HexColor("#F79A3E"), colors.HexColor("#E5484D")
BLU, LBLU = colors.HexColor("#4C9BE8"), colors.HexColor("#CFE8FF")
GRN, LGRN = colors.HexColor("#4CAF50"), colors.HexColor("#CDEFC4")
BRN, LBRN = colors.HexColor("#9C5B2E"), colors.HexColor("#E2B07A")
PNK, DPNK = colors.HexColor("#F8B4C4"), colors.HexColor("#E68AA0")
GRY, LGRY = colors.HexColor("#9AA0A6"), colors.HexColor("#E3E6EA")
BLK, PUR, SKIN = colors.HexColor("#333333"), colors.HexColor("#9B6BD6"), colors.HexColor("#F3C9A0")

ICONS = {}


def icon(name):
    def reg(fn):
        ICONS[name] = fn
        return fn
    return reg


class Pen:
    """Draw in a 100 × 100 box centered on (x, y) (coordinates -50..50)."""

    def __init__(self, c, x, y, s):
        self.c, self.x, self.y, self.u = c, x, y, s / 100.0
        self.lw = max(1.0, 2.4 * self.u)

    def p(self, px, py):
        return self.x + px * self.u, self.y + py * self.u

    def _style(self, fill, stroke=True, lw=None):
        self.c.setFillColor(fill or WHT)
        self.c.setStrokeColor(INK)
        self.c.setLineWidth(lw or self.lw)
        return 1 if stroke else 0

    def circle(self, px, py, r, fill, stroke=True):
        st = self._style(fill, stroke)
        x, y = self.p(px, py)
        self.c.circle(x, y, r * self.u, stroke=st, fill=1)

    def ellipse(self, x1, y1, x2, y2, fill, stroke=True):
        st = self._style(fill, stroke)
        a, b = self.p(x1, y1)
        d, e = self.p(x2, y2)
        self.c.ellipse(a, b, d, e, stroke=st, fill=1)

    def rect(self, x1, y1, x2, y2, fill, rad=0, stroke=True):
        st = self._style(fill, stroke)
        a, b = self.p(x1, y1)
        d, e = self.p(x2, y2)
        self.c.roundRect(a, b, d - a, e - b, rad * self.u, stroke=st, fill=1)

    def poly(self, pts, fill, stroke=True):
        st = self._style(fill, stroke)
        path = self.c.beginPath()
        for i, (px, py) in enumerate(pts):
            (path.moveTo if i == 0 else path.lineTo)(*self.p(px, py))
        path.close()
        self.c.drawPath(path, stroke=st, fill=1)

    def line(self, x1, y1, x2, y2, color=INK, lw=None):
        self.c.setStrokeColor(color)
        self.c.setLineWidth((lw or 2.4) * self.u)
        self.c.setLineCap(1)
        self.c.line(*self.p(x1, y1), *self.p(x2, y2))
        self.c.setLineCap(0)

    def curve(self, pts, color=INK, lw=None, fill=None):
        path = self.c.beginPath()
        path.moveTo(*self.p(*pts[0]))
        for i in range(1, len(pts), 3):
            path.curveTo(*self.p(*pts[i]), *self.p(*pts[i + 1]), *self.p(*pts[i + 2]))
        self.c.setStrokeColor(color)
        self.c.setLineWidth((lw or 2.4) * self.u)
        self.c.setLineCap(1)
        if fill is not None:
            self.c.setFillColor(fill)
            path.close()
        self.c.drawPath(path, stroke=1, fill=1 if fill is not None else 0)
        self.c.setLineCap(0)

    def text(self, px, py, s, size, color=INK, font="Kid-Bold"):
        self.c.setFillColor(color)
        self.c.setFont(font, size * self.u)
        self.c.drawCentredString(*self.p(px, py), s)


def wheels(pen, xs, y, r):
    for x in xs:
        pen.circle(x, y, r, BLK)
        pen.circle(x, y, r * 0.4, GRY)


# ---------------------------------------------------------------- short a
@icon("cat")
def cat(c, x, y, s):
    p = Pen(c, x, y, s)
    p.poly([(-32, 14), (-38, 46), (-8, 30)], ORG)
    p.poly([(32, 14), (38, 46), (8, 30)], ORG)
    p.circle(0, 0, 34, ORG)
    p.poly([(-28, 20), (-33, 38), (-15, 28)], PNK, stroke=False)
    p.poly([(28, 20), (33, 38), (15, 28)], PNK, stroke=False)
    p.circle(-12, 6, 4.5, BLK, stroke=False)
    p.circle(12, 6, 4.5, BLK, stroke=False)
    p.poly([(-5, -5), (5, -5), (0, -11)], DPNK)
    p.line(0, -11, -6, -18)
    p.line(0, -11, 6, -18)
    for dy in (-6, -14):
        p.line(-12, dy, -44, dy + 4, lw=1.5)
        p.line(12, dy, 44, dy + 4, lw=1.5)


@icon("hat")
def hat(c, x, y, s):
    p = Pen(c, x, y, s)
    p.rect(-26, -24, 26, 34, PUR, 3)
    p.rect(-26, -16, 26, -4, RED, stroke=False)
    p.ellipse(-46, -32, 46, -16, PUR)


@icon("rat")
def rat(c, x, y, s):
    p = Pen(c, x, y, s)
    p.curve([(30, -18), (50, -20), (50, 10), (40, 20)], DPNK, 3)
    p.ellipse(-28, -28, 36, 10, GRY)
    p.circle(-26, -4, 18, GRY)
    p.circle(-20, 14, 10, PNK)
    p.circle(-32, 0, 3, BLK, stroke=False)
    p.circle(-44, -8, 4, DPNK)
    p.ellipse(-10, -34, 2, -26, GRY)
    p.ellipse(16, -34, 28, -26, GRY)


@icon("bat")
def bat(c, x, y, s):
    p = Pen(c, x, y, s)
    p.poly([(-44, -34), (-36, -42), (40, 22), (24, 38)], LBRN)
    p.circle(-42, -40, 6, BRN)
    p.circle(28, -24, 14, WHT)
    p.curve([(20, -14), (24, -20), (24, -28), (20, -34)], RED, 1.5)
    p.curve([(36, -14), (32, -20), (32, -28), (36, -34)], RED, 1.5)


@icon("van")
def van(c, x, y, s):
    p = Pen(c, x, y, s)
    p.poly([(-46, -18), (46, -18), (46, 10), (28, 30), (-46, 30)], BLU)
    p.rect(-38, 8, -12, 24, LBLU, 2)
    p.rect(-6, 8, 18, 24, LBLU, 2)
    p.poly([(24, 8), (40, 8), (26, 24)], LBLU)
    p.circle(42, -6, 3, YEL)
    wheels(p, (-26, 26), -20, 11)


@icon("can")
def can(c, x, y, s):
    p = Pen(c, x, y, s)
    p.rect(-25, -36, 25, 30, LGRY)
    p.rect(-25, -16, 25, 12, RED, stroke=False)
    p.ellipse(-25, 22, 25, 38, GRY)
    p.ellipse(-25, -42, 25, -30, LGRY)
    p.rect(-24, -36, 24, -32, LGRY, stroke=False)


@icon("fan")
def fan(c, x, y, s):
    p = Pen(c, x, y, s)
    p.rect(-4, -38, 4, -8, GRY)
    p.ellipse(-26, -46, 26, -34, GRY)
    p.circle(0, 12, 34, LBLU)
    cx, cy = p.p(0, 12)
    for ang in (90, 210, 330):
        c.saveState()
        c.translate(cx, cy)
        c.rotate(ang)
        c.setFillColor(BLU)
        c.setStrokeColor(INK)
        c.setLineWidth(p.lw)
        c.ellipse(2 * p.u, -8 * p.u, 30 * p.u, 8 * p.u, stroke=1, fill=1)
        c.restoreState()
    p.circle(0, 12, 6, GRY)


@icon("pan")
def pan(c, x, y, s):
    p = Pen(c, x, y, s)
    p.rect(20, -6, 54, 4, BLK, 3)
    p.ellipse(-48, -24, 26, 18, GRY)
    p.ellipse(-41, -17, 19, 11, LGRY)


@icon("map")
def map_(c, x, y, s):
    p = Pen(c, x, y, s)
    p.poly([(-45, -32), (-15, -40), (-15, 32), (-45, 40)], LGRN)
    p.poly([(-15, -40), (15, -32), (15, 40), (-15, 32)], colors.HexColor("#E8F7E0"))
    p.poly([(15, -32), (45, -40), (45, 32), (15, 40)], LGRN)
    c.setDash(3, 3)
    p.curve([(-36, -22), (-20, 0), (0, -20), (10, 6), (18, 26), (28, 10), (32, 18)], RED, 2.2)
    c.setDash()
    p.line(28, 14, 38, 24, RED, 3.5)
    p.line(38, 14, 28, 24, RED, 3.5)


@icon("bag")
def bag(c, x, y, s):
    p = Pen(c, x, y, s)
    p.curve([(-14, 20), (-14, 50), (14, 50), (14, 20)], BRN, 4)
    p.poly([(-32, -40), (32, -40), (26, 22), (-26, 22)], ORG)


@icon("cap")
def cap(c, x, y, s):
    p = Pen(c, x, y, s)
    p.ellipse(4, -18, 54, -4, BLU)
    p._style(RED)
    path = c.beginPath()
    path.moveTo(*p.p(-36, -12))
    path.arcTo(*p.p(-36, -48), *p.p(36, 24), startAng=0, extent=180)
    path.close()
    c.drawPath(path, stroke=1, fill=1)
    p.circle(0, 26, 4, RED)


@icon("man")
def man(c, x, y, s):
    p = Pen(c, x, y, s)
    p.rect(-14, -46, -3, -12, BLU, 3)
    p.rect(3, -46, 14, -12, BLU, 3)
    p.line(-18, 10, -32, -16, SKIN, 7)
    p.line(18, 10, 32, -16, SKIN, 7)
    p.rect(-18, -16, 18, 18, GRN, 6)
    p.circle(0, 32, 14, SKIN)
    p.circle(-5, 34, 2, BLK, stroke=False)
    p.circle(5, 34, 2, BLK, stroke=False)
    p.curve([(-5, 27), (-2, 24), (2, 24), (5, 27)], INK, 1.5)


# ---------------------------------------------------------------- short o
@icon("dog")
def dog(c, x, y, s):
    p = Pen(c, x, y, s)
    p.circle(0, 2, 32, LBRN)
    p.ellipse(-44, -18, -22, 28, BRN)
    p.ellipse(22, -18, 44, 28, BRN)
    p.circle(-11, 10, 4.5, BLK, stroke=False)
    p.circle(11, 10, 4.5, BLK, stroke=False)
    p.ellipse(-12, -26, 12, -4, WHT, stroke=False)
    p.ellipse(-7, -10, 7, -1, BLK)
    p.ellipse(-5, -28, 5, -16, PNK)
    p.line(0, -10, 0, -18)


@icon("log")
def log(c, x, y, s):
    p = Pen(c, x, y, s)
    p.rect(-42, -18, 34, 18, BRN)
    p.line(-34, 8, -6, 8, colors.HexColor("#6E3E1C"), 2)
    p.line(-26, -6, 10, -6, colors.HexColor("#6E3E1C"), 2)
    p.ellipse(24, -18, 46, 18, LBRN)
    p.ellipse(29, -10, 41, 10, colors.HexColor("#F0CFA0"))
    p.circle(35, 0, 2, BRN, stroke=False)


@icon("box")
def box(c, x, y, s):
    p = Pen(c, x, y, s)
    p.rect(-34, -38, 20, 14, LBRN)
    p.poly([(-34, 14), (20, 14), (38, 32), (-16, 32)], colors.HexColor("#F0C890"))
    p.poly([(20, -38), (38, -20), (38, 32), (20, 14)], colors.HexColor("#C98F55"))
    p.line(-7, 14, 11, 32, BRN, 4)
    p.line(-7, 14, -7, -6, BRN, 4)


@icon("pot")
def pot(c, x, y, s):
    p = Pen(c, x, y, s)
    for dx in (-14, 0, 14):
        p.curve([(dx, 30), (dx - 6, 36), (dx + 6, 42), (dx, 48)], GRY, 2)
    p.rect(-46, -2, -34, 6, BLK, 2)
    p.rect(34, -2, 46, 6, BLK, 2)
    p.rect(-36, -34, 36, 12, GRY, 8)
    p.ellipse(-40, 8, 40, 22, LGRY)
    p.circle(0, 24, 5, BLK)


@icon("dot")
def dot(c, x, y, s):
    p = Pen(c, x, y, s)
    p.circle(0, 0, 34, RED)
    p.circle(-10, 12, 8, colors.HexColor("#F59A9D"), stroke=False)


@icon("hot")
def hot(c, x, y, s):
    p = Pen(c, x, y, s)
    flame = [(0, 46), (26, 16), (36, -12), (20, -36), (8, -48), (-8, -48), (-20, -36), (-36, -12), (-24, 14), (0, 46)]
    p.curve(flame, INK, 2.4, ORG)
    p.curve([(0, 18), (12, 2), (18, -14), (10, -28), (4, -36), (-4, -36), (-10, -28),
             (-18, -14), (-12, 2), (0, 18)], YEL, 0.1, YEL)


@icon("mop")
def mop(c, x, y, s):
    p = Pen(c, x, y, s)
    p.line(24, 48, -2, -14, BRN, 6)
    for i in range(7):
        x0 = -18 + i * 5
        p.line(x0, -20, x0 - 10 + i * 3, -46, BLU, 4)
    p.rect(-20, -22, 14, -12, GRY, 2)


@icon("top")
def top(c, x, y, s):
    p = Pen(c, x, y, s)
    p.rect(-5, 8, 5, 34, BRN, 2)
    p.poly([(0, -44), (-38, 0), (-34, 12), (34, 12), (38, 0)], RED)
    p.poly([(-30, -8), (30, -8), (22, -18), (-22, -18)], YEL, stroke=False)
    p.curve([(-46, 22), (-40, 30), (-30, 34), (-20, 34)], GRY, 2)
    p.curve([(46, 22), (40, 30), (30, 34), (20, 34)], GRY, 2)


# ---------------------------------------------------------------- short i
@icon("pig")
def pig(c, x, y, s):
    p = Pen(c, x, y, s)
    p.poly([(-30, 16), (-34, 44), (-10, 30)], PNK)
    p.poly([(30, 16), (34, 44), (10, 30)], PNK)
    p.circle(0, 0, 33, PNK)
    p.circle(-12, 10, 4, BLK, stroke=False)
    p.circle(12, 10, 4, BLK, stroke=False)
    p.ellipse(-15, -20, 15, 0, DPNK)
    p.ellipse(-8, -13, -3, -6, BLK, stroke=False)
    p.ellipse(3, -13, 8, -6, BLK, stroke=False)


@icon("wig")
def wig(c, x, y, s):
    p = Pen(c, x, y, s)
    p.rect(-8, -46, 8, -28, LGRY)
    for ang in range(-30, 211, 20):
        r = math.radians(ang)
        p.circle(30 * math.cos(r), 4 + 30 * math.sin(r), 12, ORG)
    p.ellipse(-20, -34, 20, 20, SKIN)
    for ang in range(20, 161, 28):
        r = math.radians(ang)
        p.circle(24 * math.cos(r), 10 + 22 * math.sin(r), 10, ORG)
    p.circle(-7, -6, 2.5, BLK, stroke=False)
    p.circle(7, -6, 2.5, BLK, stroke=False)


@icon("dig")
def dig(c, x, y, s):
    p = Pen(c, x, y, s)
    p.poly([(-50, -46), (-40, -30), (-20, -24), (2, -34), (10, -46)], BRN)
    p.line(30, 46, 2, 0, BRN, 6)
    p.line(22, 48, 38, 44, BRN, 6)
    p.poly([(-12, 8), (12, -6), (0, -36), (-26, -20)], GRY)


@icon("lid")
def lid(c, x, y, s):
    p = Pen(c, x, y, s)
    p.rect(-24, -44, 24, 8, colors.HexColor("#E6F4FF"), 8)
    p.rect(-18, 8, 18, 14, colors.HexColor("#E6F4FF"))
    p.rect(-26, 26, 26, 40, RED, 4)
    p.line(-34, 30, -40, 26, GRY, 2)
    p.line(34, 30, 40, 26, GRY, 2)


@icon("pin")
def pin(c, x, y, s):
    p = Pen(c, x, y, s)
    p.line(0, -4, 0, -46, GRY, 3)
    p.rect(-10, -6, 10, 6, DPNK, 2)
    p.ellipse(-22, 4, 22, 16, RED)
    p.rect(-9, 14, 9, 30, RED, 2)
    p.ellipse(-18, 26, 18, 40, RED)


@icon("bin")
def bin_(c, x, y, s):
    p = Pen(c, x, y, s)
    p.poly([(-28, -42), (28, -42), (34, 20), (-34, 20)], GRN)
    for dx in (-14, 0, 14):
        p.line(dx, -34, dx * 1.15, 12, colors.HexColor("#2E7D32"), 2)
    p.rect(-40, 20, 40, 30, colors.HexColor("#3E9B43"), 3)
    p.rect(-8, 30, 8, 36, colors.HexColor("#3E9B43"), 2)


@icon("fin")
def fin(c, x, y, s):
    p = Pen(c, x, y, s)
    p.rect(-48, -40, 48, -6, LBLU, stroke=False)
    p.curve([(-22, -8), (-10, 10), (6, 30), (18, 44), (16, 20), (18, 4), (26, -8)], INK, 2.4, GRY)
    for yy in (-8, -22):
        p.curve([(-48, yy), (-36, yy + 6), (-24, yy - 6), (-12, yy), (0, yy + 6), (12, yy - 6), (24, yy),
                 (36, yy + 6), (42, yy - 4), (48, yy)], BLU, 2.4)


@icon("six")
def six(c, x, y, s):
    p = Pen(c, x, y, s)
    p.rect(-38, -38, 38, 38, WHT, 12)
    for dx in (-18, 18):
        for dy in (-20, 0, 20):
            p.circle(dx, dy, 7, RED, stroke=False)


# ---------------------------------------------------------------- short u
@icon("bus")
def bus(c, x, y, s):
    p = Pen(c, x, y, s)
    p.rect(-48, -20, 48, 28, YEL, 7)
    for i in range(4):
        p.rect(-42 + i * 18, 6, -30 + i * 18, 22, LBLU, 2)
    p.rect(30, -6, 44, 22, LBLU, 2)
    p.line(-48, -4, 48, -4, BLK, 2)
    p.circle(45, -12, 3, ORG)
    wheels(p, (-28, 26), -22, 10)


@icon("sun")
def sun(c, x, y, s):
    p = Pen(c, x, y, s)
    for i in range(12):
        a = math.radians(i * 30)
        p.line(36 * math.cos(a), 36 * math.sin(a), 48 * math.cos(a), 48 * math.sin(a), ORG, 5)
    p.circle(0, 0, 28, YEL)
    p.circle(-9, 6, 3, BLK, stroke=False)
    p.circle(9, 6, 3, BLK, stroke=False)
    p.curve([(-11, -8), (-5, -15), (5, -15), (11, -8)], INK, 2)


@icon("cup")
def cup(c, x, y, s):
    p = Pen(c, x, y, s)
    c.setStrokeColor(INK)
    c.setLineWidth(9 * p.u)
    c.circle(*p.p(26, 2), 13 * p.u, stroke=1, fill=0)
    c.setStrokeColor(RED)
    c.setLineWidth(5 * p.u)
    c.circle(*p.p(26, 2), 13 * p.u, stroke=1, fill=0)
    p.poly([(-28, 30), (28, 30), (20, -34), (-20, -34)], RED)
    p.rect(-20, 18, 20, 22, WHT, stroke=False)


@icon("bug")
def bug(c, x, y, s):
    p = Pen(c, x, y, s)
    for dy in (-20, -4, 12):
        p.line(-26, dy, -42, dy - 6)
        p.line(26, dy, 42, dy - 6)
    p.circle(0, 26, 15, BLK)
    p.circle(-5, 32, 3, WHT, stroke=False)
    p.circle(5, 32, 3, WHT, stroke=False)
    p.circle(0, -6, 30, RED)
    p.line(0, 24, 0, -36, BLK, 2.4)
    for dx, dy in ((-14, 4), (14, 4), (-12, -18), (12, -18)):
        p.circle(dx, dy, 6, BLK, stroke=False)


@icon("nut")
def nut(c, x, y, s):
    p = Pen(c, x, y, s)
    p.poly([(36 * math.cos(math.radians(a)), 36 * math.sin(math.radians(a))) for a in range(0, 360, 60)], GRY)
    p.poly([(28 * math.cos(math.radians(a)), 28 * math.sin(math.radians(a))) for a in range(0, 360, 60)], LGRY)
    p.circle(0, 0, 14, WHT)


@icon("rug")
def rug(c, x, y, s):
    p = Pen(c, x, y, s)
    for yy in range(-24, 25, 6):
        p.line(-48, yy, -42, yy, BRN, 1.6)
        p.line(42, yy, 48, yy, BRN, 1.6)
    p.rect(-42, -28, 42, 28, RED, 3)
    p.rect(-32, -18, 32, 18, YEL, stroke=False)
    p.poly([(0, -12), (16, 0), (0, 12), (-16, 0)], BLU)


@icon("tub")
def tub(c, x, y, s):
    p = Pen(c, x, y, s)
    for dx, dy, r in ((-24, 12, 9), (-8, 18, 11), (10, 14, 9), (24, 20, 7), (-30, 24, 6)):
        p.circle(dx, dy, r, colors.HexColor("#F2FAFF"))
    p.line(36, 8, 36, 30, GRY, 4)
    p.line(36, 30, 28, 30, GRY, 4)
    p.rect(-46, -22, 46, 8, colors.HexColor("#F2FAFF"), 10)
    p.rect(-46, 2, 46, 8, LBLU, stroke=False)
    p.line(-30, -22, -34, -36, BLK, 4)
    p.line(30, -22, 34, -36, BLK, 4)


@icon("hut")
def hut(c, x, y, s):
    p = Pen(c, x, y, s)
    p.rect(-32, -40, 32, 6, LBRN)
    p.poly([(-46, 4), (46, 4), (0, 44)], colors.HexColor("#D4A537"))
    for dx in (-24, -10, 4, 18):
        p.line(dx, 8, dx * 0.5, 30, BRN, 1.5)
    p.rect(-9, -40, 9, -12, BRN, 3)


# ---------------------------------------------------------------- short e
@icon("bed")
def bed(c, x, y, s):
    p = Pen(c, x, y, s)
    p.rect(-46, -32, -36, 26, BRN, 2)
    p.rect(-36, -18, 46, -4, WHT)
    p.rect(-8, -18, 46, 4, BLU, 3)
    p.ellipse(-34, -4, -10, 10, WHT)
    p.line(42, -18, 42, -32, BRN, 4)


@icon("hen")
def hen(c, x, y, s):
    p = Pen(c, x, y, s)
    p.line(-6, -26, -10, -44, ORG, 3)
    p.line(10, -26, 6, -44, ORG, 3)
    p.poly([(-44, 10), (-30, 0), (-40, -10)], WHT)
    p.ellipse(-36, -30, 26, 14, WHT)
    p.circle(20, 20, 15, WHT)
    p.circle(16, 37, 5, RED, stroke=False)
    p.circle(23, 38, 5, RED, stroke=False)
    p.poly([(34, 22), (44, 18), (34, 14)], ORG)
    p.circle(23, 23, 2.5, BLK, stroke=False)
    p.curve([(-18, 0), (-8, -14), (6, -12), (10, -2)], INK, 2)


@icon("net")
def net(c, x, y, s):
    p = Pen(c, x, y, s)
    p.line(14, -18, 40, -48, BRN, 6)
    cx, cy = p.p(-6, 12)
    r = 30 * p.u
    c.saveState()
    path = c.beginPath()
    path.circle(cx, cy, r)
    c.clipPath(path, stroke=0, fill=0)
    c.setStrokeColor(GRY)
    c.setLineWidth(1)
    k = -r
    while k <= r:
        c.line(cx + k, cy - r, cx + k, cy + r)
        c.line(cx - r, cy + k, cx + r, cy + k)
        k += 8 * p.u
    c.restoreState()
    c.setStrokeColor(GRN)
    c.setLineWidth(4 * p.u)
    c.circle(cx, cy, r, stroke=1, fill=0)


@icon("pen")
def pen(c, x, y, s):
    p = Pen(c, x, y, s)
    c.saveState()
    c.translate(x, y)
    c.rotate(35)
    q = Pen(c, 0, 0, s)
    q.rect(-44, -7, 22, 7, BLU, 3)
    q.poly([(22, -7), (22, 7), (42, 0)], colors.HexColor("#F0D6B0"))
    q.poly([(36, -2), (36, 2), (42, 0)], BLK, stroke=False)
    q.rect(-30, 7, -6, 10, GRY, 1)
    c.restoreState()
    del p


@icon("jet")
def jet(c, x, y, s):
    c.saveState()
    c.translate(x, y)
    c.rotate(20)
    p = Pen(c, 0, 0, s)
    p.poly([(-4, 0), (14, 0), (-14, 40), (-24, 40)], LGRY)
    p.poly([(-38, 0), (-30, 0), (-44, 22), (-50, 22)], LGRY)
    p.ellipse(-50, -9, 48, 9, WHT)
    p.poly([(-4, 0), (14, 0), (-14, -40), (-24, -40)], LGRY)
    for dx in (-24, -14, -4, 6, 16):
        p.circle(dx, 2, 2.5, BLU, stroke=False)
    p.circle(36, 2, 3, BLU, stroke=False)
    c.restoreState()


@icon("web")
def web(c, x, y, s):
    p = Pen(c, x, y, s)
    for i in range(8):
        a = math.radians(i * 45 + 22.5)
        p.line(0, 0, 46 * math.cos(a), 46 * math.sin(a), GRY, 1.6)
    for r in (12, 24, 36):
        pts = [(r * math.cos(math.radians(i * 45 + 22.5)), r * math.sin(math.radians(i * 45 + 22.5))) for i in range(8)]
        for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1]):
            p.line(x1, y1, x2, y2, GRY, 1.6)
    p.line(20, 46, 20, -14, INK, 1)
    p.circle(20, -18, 7, BLK)


@icon("ten")
def ten(c, x, y, s):
    p = Pen(c, x, y, s)
    p.rect(-46, -20, 46, 20, WHT, 3)
    for i in range(1, 5):
        p.line(-46 + i * 18.4, -20, -46 + i * 18.4, 20, INK, 1.4)
    p.line(-46, 0, 46, 0, INK, 1.4)
    for i in range(5):
        for j in range(2):
            p.circle(-36.8 + i * 18.4, -10 + j * 20, 6.5, BLU, stroke=False)


@icon("leg")
def leg(c, x, y, s):
    p = Pen(c, x, y, s)
    p.poly([(-16, 46), (10, 46), (8, 0), (10, -26), (-12, -26), (-14, 0)], SKIN)
    p.rect(-14, -44, 30, -24, RED, 6)
    p.line(-2, -24, 10, -32, WHT, 2)


# ---------------------------------------------------------------- vowel pictures
@icon("apple")
def apple(c, x, y, s):
    p = Pen(c, x, y, s)
    p.line(0, 24, 4, 42, BRN, 4)
    p.ellipse(6, 26, 30, 38, GRN)
    p.circle(-12, -4, 27, RED)
    p.circle(12, -4, 27, RED)
    p.circle(-12, -4, 25, RED, stroke=False)
    p.circle(-16, 6, 6, colors.HexColor("#F59A9D"), stroke=False)


@icon("egg")
def egg(c, x, y, s):
    p = Pen(c, x, y, s)
    p.ellipse(-26, -36, 26, 38, colors.HexColor("#FFF7E8"))
    p.ellipse(-14, 8, -6, 22, WHT, stroke=False)


@icon("igloo")
def igloo(c, x, y, s):
    p = Pen(c, x, y, s)
    p._style(colors.HexColor("#EEF7FF"))
    path = c.beginPath()
    path.moveTo(*p.p(-44, -30))
    path.arcTo(*p.p(-44, -74), *p.p(44, 14), startAng=0, extent=180)
    path.close()
    c.drawPath(path, stroke=1, fill=1)
    for yy in (-14, 2):
        p.line(-40 + (yy + 30) * 0.2, yy, 40 - (yy + 30) * 0.2, yy, LBLU, 1.6)
    p._style(BLU)
    path = c.beginPath()
    path.moveTo(*p.p(-12, -30))
    path.arcTo(*p.p(-12, -42), *p.p(12, -6), startAng=0, extent=180)
    path.close()
    c.drawPath(path, stroke=1, fill=1)


@icon("octopus")
def octopus(c, x, y, s):
    p = Pen(c, x, y, s)
    for i, dx in enumerate((-30, -18, -6, 6, 18, 30)):
        bend = 10 if i % 2 else -10
        p.curve([(dx * 0.7, -6), (dx, -24), (dx + bend, -34), (dx + bend * 0.4, -46)], PUR, 7)
    p.ellipse(-30, -16, 30, 42, PUR)
    p.circle(-10, 14, 6, WHT)
    p.circle(10, 14, 6, WHT)
    p.circle(-10, 14, 3, BLK, stroke=False)
    p.circle(10, 14, 3, BLK, stroke=False)


@icon("umbrella")
def umbrella(c, x, y, s):
    p = Pen(c, x, y, s)
    p.line(0, 4, 0, -36, BLK, 3.5)
    p.curve([(0, -36), (0, -46), (-12, -46), (-12, -38)], BLK, 3.5)
    p._style(RED)
    path = c.beginPath()
    path.moveTo(*p.p(-46, 4))
    path.arcTo(*p.p(-46, -42), *p.p(46, 50), startAng=180, extent=-180)
    for i in range(4):
        x0 = 46 - i * 23
        path.curveTo(*p.p(x0 - 6, 12), *p.p(x0 - 17, 12), *p.p(x0 - 23, 4))
    path.close()
    c.drawPath(path, stroke=1, fill=1)
    p.circle(0, 50, 3, BLK)


# ---------------------------------------------------------------- theme pictures
@icon("engine")
def engine(c, x, y, s):
    p = Pen(c, x, y, s)
    p.rect(-26, 18, -12, 40, BLK, 2)
    p.rect(-40, -20, 20, 18, RED, 4)
    p.rect(14, -20, 46, 34, BLU, 3)
    p.rect(22, 10, 38, 26, LBLU, 2)
    p.poly([(-40, -20), (-50, -20), (-40, -6)], GRY)
    p.circle(-36, 10, 5, YEL)
    wheels(p, (-26, 0, 30), -24, 10)


@icon("traincar")
def traincar(c, x, y, s):
    p = Pen(c, x, y, s)
    p.line(-50, -14, 50, -14, GRY, 4)
    p.rect(-44, -18, 44, 28, YEL, 4)
    wheels(p, (-26, 26), -22, 9)


@icon("car")
def car(c, x, y, s):
    p = Pen(c, x, y, s)
    p.poly([(-22, 6), (-12, 26), (16, 26), (28, 6)], LBLU)
    p.rect(-48, -18, 48, 8, RED, 8)
    p.line(2, 26, 2, 6, INK, 2.4)
    p.circle(44, -2, 3, YEL)
    wheels(p, (-26, 26), -20, 11)


@icon("solar")
def solar(c, x, y, s):
    p = Pen(c, x, y, s)
    p.line(0, -16, 0, -44, GRY, 5)
    p.rect(-22, -48, 22, -42, GRY, 2)
    p.poly([(-44, -16), (36, -16), (46, 30), (-30, 30)], colors.HexColor("#1F4E8C"))
    for t in (1 / 3, 2 / 3):
        p.line(-44 + 14 * t * 3, -16 + 46 * t, 36 + 10 * t * 3 / 3 * 1, -16 + 46 * t, LBLU, 1.5)
    for k in range(1, 4):
        x0 = -44 + 80 * k / 4
        p.line(x0, -16, x0 + 14, 30, LBLU, 1.5)
    p.circle(38, 42, 9, YEL)


@icon("bulb")
def bulb(c, x, y, s):
    p = Pen(c, x, y, s)
    p.rect(-12, -44, 12, -20, GRY, 3)
    for yy in (-36, -28):
        p.line(-12, yy, 12, yy, INK, 1.6)
    p.circle(0, 8, 28, WHT)
    p.curve([(-6, -16), (-6, 0), (-10, 4), (-4, 10)], GRY, 1.6)
    p.curve([(6, -16), (6, 0), (10, 4), (4, 10)], GRY, 1.6)


@icon("toolbox")
def toolbox(c, x, y, s):
    p = Pen(c, x, y, s)
    p.rect(-14, 10, 14, 26, None, 4)
    p.rect(-10, 10, 10, 22, WHT, 2, stroke=False)
    p.rect(-44, -34, 44, 14, RED, 4)
    p.rect(-44, -4, 44, 2, colors.HexColor("#B8323A"), stroke=False)
    p.rect(-8, -10, 8, 4, GRY, 2)


@icon("wrench")
def wrench(c, x, y, s):
    p = Pen(c, x, y, s)
    c.saveState()
    c.translate(x, y)
    c.rotate(-40)
    q = Pen(c, 0, 0, s)
    q.rect(-40, -6, 22, 6, GRY, 3)
    q.circle(28, 0, 14, GRY)
    q.rect(26, -5, 46, 5, WHT, stroke=False)
    q.circle(-40, 0, 9, GRY)
    c.restoreState()


@icon("mouse")
def mouse(c, x, y, s):
    p = Pen(c, x, y, s)
    p.curve([(0, 36), (0, 48), (24, 44), (30, 50)], INK, 2)
    p.rect(-22, -40, 22, 36, LGRY, 20)
    p.line(0, 36, 0, 6)
    p.line(-22, 6, 22, 6)
    p.rect(-3, 14, 3, 28, GRY, 2)


def draw_icon(c, name, x, y, s):
    ICONS[name](c, x, y, s)
