"""Shared toolkit for the printable worksheet books in this repo.

Every book's build.py does `from common.printkit import *` and gets:
  * page setup (US Letter, 0.5" margins), kid-friendly fonts (DejaVu Sans as "Kid"), color themes TH
  * worksheet chrome: header(), footer(), section(), tip(), card(), write_line()
  * math sentences and drills: expr(), vdrill(), hdrill(), vdrill_page(), hdrill_page()
  * pictures: draw_groups(), draw_array(), numberline(), jumps_back(), area_grid(), triangle(), mult_chart(),
    cookie(), plate(), star(), arrow(), word_card()
  * problem generators: pick(), pool(), h_mul(), h_div(), h_miss(), h_div_missing(), mixed_items(), div_facts()
  * book assembly: Page (full-page flowable), ST/P/bullets/table (parent-guide text), section_title(),
    KEY + key_story() (answer key), build_pdf()

Any page function that generates problems should append (title, [answers]) to KEY so the answer key matches.
"""
import math
import os
import random

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily, stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Flowable, Frame, KeepTogether, PageBreak,
                                PageTemplate, Paragraph, Spacer, Table, TableStyle)

# ---------------------------------------------------------------- setup
FONT_DIR = os.environ.get("KID_FONT_DIR", "/usr/share/fonts/truetype/dejavu/")
pdfmetrics.registerFont(TTFont("Kid", FONT_DIR + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("Kid-Bold", FONT_DIR + "DejaVuSans-Bold.ttf"))
registerFontFamily("Kid", normal="Kid", bold="Kid-Bold", italic="Kid", boldItalic="Kid-Bold")
R, B = "Kid", "Kid-Bold"

PAGE_W, PAGE_H = letter
MARGIN = 36
FW, FH = PAGE_W - 2 * MARGIN, PAGE_H - 2 * MARGIN

INK = colors.HexColor("#222222")
GRAY = colors.HexColor("#8a8a8a")
WHITE = colors.white
TH = {
    1: (colors.HexColor("#E3F0FB"), colors.HexColor("#2F6FB3")),
    2: (colors.HexColor("#E4F4E6"), colors.HexColor("#2E8540")),
    3: (colors.HexColor("#FFEFDC"), colors.HexColor("#BF6206")),
    4: (colors.HexColor("#EFE7FA"), colors.HexColor("#7040AD")),
    "x": (colors.HexColor("#DFF3F3"), colors.HexColor("#1B7A7B")),
    "t": (colors.HexColor("#FCE6E6"), colors.HexColor("#B32F2F")),
}

COOKIE, CHIP = colors.HexColor("#F3D9A4"), colors.HexColor("#8A5A1E")

BOX, CIRC = "<box>", "<circle>"
KEY = []  # (title, [answers]) in book order


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------------------------------------------------------------- drawing helpers
def text(c, x, y, s, size=12, font=R, color=INK, align="l"):
    c.setFont(font, size)
    c.setFillColor(color)
    {"l": c.drawString, "c": c.drawCentredString, "r": c.drawRightString}[align](x, y, str(s))


def para(c, x, y, s, width, size=11, font=R, color=INK, leading=None):
    leading = leading or size * 1.3
    for line in simpleSplit(s, font, size, width):
        text(c, x, y, line, size, font, color)
        y -= leading
    return y


def card(c, x, y, w, h, theme, fill=False, radius=8):
    light, dark = theme
    c.setStrokeColor(dark)
    c.setLineWidth(0.9)
    c.setFillColor(light if fill else WHITE)
    c.roundRect(x, y, w, h, radius, stroke=1, fill=1)


def write_line(c, x, y, x2, label=None, size=10.5):
    if label:
        text(c, x, y, label, size, B)
        x += stringWidth(label, B, size) + 6
    c.setStrokeColor(INK)
    c.setLineWidth(0.8)
    c.line(x, y - 2, x2, y - 2)


def header(c, W, H, theme, tag, title, instr=None):
    light, dark = theme
    c.setLineWidth(1.5)
    c.setStrokeColor(dark)
    c.setFillColor(light)
    c.roundRect(0, H - 56, W, 56, 10, stroke=1, fill=1)
    text(c, 14, H - 18, tag.upper(), 9.5, B, dark)
    text(c, 14, H - 45, title, 21, B)
    text(c, W - 14, H - 45, "★", 22, B, dark, "r")
    y = H - 80
    write_line(c, 0, y, 300, "Name:", 11)
    write_line(c, 330, y, W, "Date:", 11)
    y -= 24
    if instr:
        y = para(c, 0, y, instr, W, 11.5, leading=15)
    return y - 4


def footer(c, W, total=None, timed=False):
    c.setStrokeColor(GRAY)
    c.setLineWidth(0.6)
    c.line(0, 24, W, 24)
    text(c, 0, 8, f"Score: ______ / {total}" if total else "Score: ________", 10.5, B)
    if timed:
        text(c, W / 2, 8, "Time: __________", 10.5, B, align="c")
    text(c, W, 8, "Parent check  ☐", 10.5, B, align="r")


def section(c, y, letter_, label, theme):
    c.setFillColor(theme[1])
    c.roundRect(0, y - 16, 22, 18, 4, stroke=0, fill=1)
    text(c, 11, y - 11.5, letter_, 11, B, WHITE, "c")
    text(c, 30, y - 12, label, 12.5, B)
    return y - 28


def tip(c, y, W, theme, lines, size=11, h=None):
    """Shaded hint box. lines: str or (bold_prefix, rest)."""
    lead = size * 1.4
    h = h or len(lines) * lead + 14
    card(c, 0, y - h, W, h, theme, fill=True)
    yy = y - 10 - size
    for ln in lines:
        if isinstance(ln, tuple):
            text(c, 12, yy, ln[0], size, B, theme[1])
            text(c, 12 + stringWidth(ln[0], B, size) + 5, yy, ln[1], size)
        else:
            text(c, 12, yy, ln, size)
        yy -= lead
    return y - h - 10


def expr(c, x, y, toks, size=16, box_w=None):
    """Draw a math sentence on baseline y. BOX = answer box, CIRC = circle for <,>,=."""
    bw = box_w or size * 2.3
    gap = size * 0.3
    for t in toks:
        if t == BOX:
            c.setStrokeColor(INK)
            c.setLineWidth(1)
            c.roundRect(x, y - size * 0.35, bw, size * 1.45, 4, stroke=1, fill=0)
            x += bw + gap
        elif t == CIRC:
            r = size * 0.72
            c.setStrokeColor(INK)
            c.setLineWidth(1)
            c.circle(x + r, y + size * 0.36, r, stroke=1, fill=0)
            x += 2 * r + gap
        else:
            text(c, x, y, t, size)
            x += stringWidth(str(t), R, size) + gap
    return x


def vdrill(c, probs, top, W, cols, cell_h, size=19, op="×"):
    cw = W / cols
    for i, (a, b) in enumerate(probs):
        r, k = divmod(i, cols)
        x, y = k * cw, top - r * cell_h
        right = x + cw * 0.74
        text(c, x + 3, y - 9, f"{i + 1}.", 7.5, R, GRAY)
        text(c, right, y - size, a, size, align="r")
        text(c, right, y - 2 * size - 1, b, size, align="r")
        text(c, right - 2.35 * size, y - 2 * size - 1, op, size)
        c.setStrokeColor(INK)
        c.setLineWidth(1.3)
        c.line(right - 2.45 * size, y - 2 * size - 7, right + 3, y - 2 * size - 7)
    return top - math.ceil(len(probs) / cols) * cell_h


def hdrill(c, items, top, W, cols, cell_h, size=15, box_w=None, numbered=True):
    cw = W / cols
    for i, toks in enumerate(items):
        r, k = divmod(i, cols)
        x, y = k * cw, top - r * cell_h - size * 1.05
        if numbered:
            text(c, x, y + 1, f"{i + 1}.", 8, R, GRAY)
        expr(c, x + (18 if numbered else 0), y, toks, size, box_w)
    return top - math.ceil(len(items) / cols) * cell_h


DICE = {
    1: [(0, 0)], 2: [(-1, 1), (1, -1)], 3: [(-1, 1), (0, 0), (1, -1)],
    4: [(-1, -1), (-1, 1), (1, -1), (1, 1)], 5: [(-1, -1), (-1, 1), (1, -1), (1, 1), (0, 0)],
    6: [(-1, -1), (-1, 0), (-1, 1), (1, -1), (1, 0), (1, 1)],
}


def draw_groups(c, x, cy, w, g, n, theme, rmax=24):
    light, dark = theme
    slot = w / g
    r = min(rmax, slot * 0.42)
    for i in range(g):
        cx = x + slot * (i + 0.5)
        c.setFillColor(light)
        c.setStrokeColor(dark)
        c.setLineWidth(1.2)
        c.circle(cx, cy, r, stroke=1, fill=1)
        c.setFillColor(dark)
        d = r * 0.48
        for px, py in DICE[n]:
            c.circle(cx + px * d, cy + py * d, max(2.3, r * 0.13), stroke=0, fill=1)


def draw_array(c, x, ytop, rows, cols, step, color, split=None, color2=None):
    for i in range(rows):
        for j in range(cols):
            c.setFillColor(color2 if split is not None and j >= split else color)
            c.circle(x + step * (j + 0.5), ytop - step * (i + 0.5), step * 0.32, stroke=0, fill=1)


def numberline(c, x, y, w, maxv, jumps, size, theme):
    dark = theme[1]
    unit = w / maxv
    c.setStrokeColor(INK)
    c.setLineWidth(1.2)
    c.line(x - 4, y, x + w + 4, y)
    for v in range(maxv + 1):
        xx = x + v * unit
        t = 6 if v % 5 == 0 else 3.5
        c.setStrokeColor(INK)
        c.line(xx, y - t, xx, y + t)
        text(c, xx, y - 16, v, 8, R, INK, "c")
    for k in range(jumps):
        x0, x1 = x + k * size * unit, x + (k + 1) * size * unit
        hgt = min(30, 10 + size * unit * 0.4)
        c.setStrokeColor(dark)
        c.setLineWidth(1.5)
        p = c.beginPath()
        p.moveTo(x0, y + 2)
        p.curveTo(x0, y + hgt, x1, y + hgt, x1, y + 3)
        c.drawPath(p, stroke=1, fill=0)
        c.setFillColor(dark)
        a = c.beginPath()
        a.moveTo(x1, y + 2)
        a.lineTo(x1 - 3.5, y + 9)
        a.lineTo(x1 + 3.5, y + 9)
        a.close()
        c.drawPath(a, stroke=0, fill=1)


def area_grid(c, x, ytop, rows, cols, u, theme):
    light, dark = theme
    c.setFillColor(light)
    c.setStrokeColor(dark)
    c.setLineWidth(0.8)
    for i in range(rows):
        for j in range(cols):
            c.rect(x + j * u, ytop - (i + 1) * u, u, u, stroke=1, fill=1)
    c.setLineWidth(1.6)
    c.rect(x, ytop - rows * u, cols * u, rows * u, stroke=1, fill=0)


def triangle(c, cx, base_y, w, h, top, left, right, theme):
    light, dark = theme
    c.setFillColor(light)
    c.setStrokeColor(dark)
    c.setLineWidth(1.4)
    p = c.beginPath()
    p.moveTo(cx - w / 2, base_y)
    p.lineTo(cx + w / 2, base_y)
    p.lineTo(cx, base_y + h)
    p.close()
    c.drawPath(p, stroke=1, fill=1)
    text(c, cx, base_y + h - 26, top, 14, B, dark, "c")
    text(c, cx - w / 2 + 20, base_y + 7, left, 13, B, INK, "c")
    text(c, cx + w / 2 - 20, base_y + 7, right, 13, B, INK, "c")
    text(c, cx, base_y + h * 0.3, "× ÷", 9, R, GRAY, "c")


def mult_chart(c, x, ytop, cell, theme, filled=True, size=14):
    light, dark = theme
    for i in range(11):
        for j in range(11):
            cx, cy = x + j * cell, ytop - (i + 1) * cell
            if i == 0 or j == 0:
                c.setFillColor(dark)
            elif filled and i == j:
                c.setFillColor(light)
            else:
                c.setFillColor(WHITE)
            c.setStrokeColor(dark)
            c.setLineWidth(0.7)
            c.rect(cx, cy, cell, cell, stroke=1, fill=1)
            ty = cy + cell / 2 - size * 0.35
            if i == 0 and j == 0:
                text(c, cx + cell / 2, ty, "×", size + 2, B, WHITE, "c")
            elif i == 0 or j == 0:
                text(c, cx + cell / 2, ty, i or j, size, B, WHITE, "c")
            elif filled:
                text(c, cx + cell / 2, ty, i * j, size, R, INK, "c")


def word_card(c, x, top, w, h, n, story, theme, lines=("Number sentence:", "Answer:")):
    card(c, x, top - h, w, h, theme)
    text(c, x + 10, top - 19, f"{n}.", 12, B, theme[1])
    para(c, x + 28, top - 19, story, w - 40, 10.5, leading=14)
    ly = top - h + 16 + (len(lines) - 1) * 25
    for lab in lines:
        write_line(c, x + 12, ly, x + w - 12, lab, 10)
        ly -= 25


# ---------------------------------------------------------------- problem generators
def pick(rng, pool, n):
    out = []
    while len(out) < n:
        p = pool[:]
        rng.shuffle(p)
        out += p
    return out[:n]


def pool(cond, lo=0, hi=10):
    return [(a, b) for a in range(lo, hi + 1) for b in range(lo, hi + 1) if cond(a, b)]


def h_mul(a, b):
    return [a, "×", b, "=", BOX], a * b


def h_div(d, q):
    return [d * q, "÷", d, "=", BOX], q


def h_miss(a, b, rng):
    if rng.random() < 0.5:
        return [a, "×", BOX, "=", a * b], b
    return [BOX, "×", b, "=", a * b], a


def mixed_items(rng, n_mul, n_div, n_miss):
    items = [h_mul(a, b) for a, b in pick(rng, pool(lambda a, b: True), n_mul)]
    items += [h_div(d, q) for d, q in pick(rng, pool(lambda a, b: True, 1), n_div)]
    items += [h_miss(a, b, rng) for a, b in pick(rng, pool(lambda a, b: True, 1), n_miss)]
    rng.shuffle(items)
    return items


# ---------------------------------------------------------------- page flowable
class Page(Flowable):
    """A full page drawn directly on the canvas."""

    def __init__(self, fn):
        super().__init__()
        self.fn = fn

    def wrap(self, aw, ah):
        return FW, FH - 2

    def draw(self):
        self.fn(self.canv, FW, FH - 2)


def vdrill_page(theme, tag, title, instr, probs, cols, cell_h, key_title, size=19):
    KEY.append((key_title, [a * b for a, b in probs]))

    def draw(c, W, H):
        y = header(c, W, H, theme, tag, title, instr)
        vdrill(c, probs, y - 4, W, cols, cell_h, size)
        footer(c, W, len(probs), timed=True)
    return draw


def hdrill_page(theme, tag, title, instr, items, cols, cell_h, key_title, size=15, box_w=None):
    KEY.append((key_title, [a for _, a in items]))

    def draw(c, W, H):
        y = header(c, W, H, theme, tag, title, instr)
        hdrill(c, [t for t, _ in items], y - 4, W, cols, cell_h, size, box_w)
        footer(c, W, len(items), timed=True)
    return draw


MAD = ("Set a timer for 3 minutes and answer as many as you can. When the timer rings, "
       "draw a line, then finish the rest.   My goal: ______   My best: ______")


def cookie(c, cx, cy, r):
    c.setFillColor(COOKIE)
    c.setStrokeColor(CHIP)
    c.setLineWidth(0.8)
    c.circle(cx, cy, r, stroke=1, fill=1)
    c.setFillColor(CHIP)
    for dx, dy in ((-0.35, 0.25), (0.3, 0.3), (0.05, -0.35)):
        c.circle(cx + dx * r, cy + dy * r, r * 0.14, stroke=0, fill=1)


def plate(c, cx, cy, r):
    c.setFillColor(WHITE)
    c.setStrokeColor(GRAY)
    c.setLineWidth(1.5)
    c.circle(cx, cy, r, stroke=1, fill=1)
    c.setLineWidth(0.6)
    c.circle(cx, cy, r * 0.72, stroke=1, fill=0)


def star(c, cx, cy, r, color):
    p = c.beginPath()
    for i in range(10):
        ang = math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        x, y = cx + rr * math.cos(ang), cy + rr * math.sin(ang)
        (p.moveTo if i == 0 else p.lineTo)(x, y)
    p.close()
    c.setFillColor(color)
    c.drawPath(p, stroke=0, fill=1)


def cookie_rows(c, x, ytop, n, r=5.5, gap=15, per_row=10):
    for i in range(n):
        row, col = divmod(i, per_row)
        cookie(c, x + col * gap + r, ytop - row * gap - r, r)


def scattered_stars(c, x, ytop, n, rng, color, cols=6, gap=21):
    for i in range(n):
        row, col = divmod(i, cols)
        star(c, x + col * gap + 10 + rng.uniform(-3, 3), ytop - row * gap - 10 + rng.uniform(-3, 3), 8, color)


def jumps_back(c, x, y, w, maxv, start, size, theme):
    """Number line 0..maxv with jumps from `start` back to 0."""
    numberline(c, x, y, w, maxv, 0, 1, theme)
    unit = w / maxv
    dark = theme[1]
    v = start
    while v > 0:
        x0, x1 = x + v * unit, x + (v - size) * unit
        hgt = min(30, 10 + size * unit * 0.4)
        c.setStrokeColor(dark)
        c.setLineWidth(1.5)
        p = c.beginPath()
        p.moveTo(x0, y + 2)
        p.curveTo(x0, y + hgt, x1, y + hgt, x1, y + 3)
        c.drawPath(p, stroke=1, fill=0)
        c.setFillColor(dark)
        a = c.beginPath()
        a.moveTo(x1, y + 2)
        a.lineTo(x1 - 3.5, y + 9)
        a.lineTo(x1 + 3.5, y + 9)
        a.close()
        c.drawPath(a, stroke=0, fill=1)
        v -= size


def arrow(c, x0, y0, x1, y1, color, lw=2.5):
    c.setStrokeColor(color)
    c.setFillColor(color)
    c.setLineWidth(lw)
    c.line(x0, y0, x1, y1)
    ang = math.atan2(y1 - y0, x1 - x0)
    p = c.beginPath()
    p.moveTo(x1, y1)
    for da in (2.6, -2.6):
        p.lineTo(x1 + 10 * math.cos(ang + da), y1 + 10 * math.sin(ang + da))
    p.close()
    c.drawPath(p, stroke=0, fill=1)


# ---------------------------------------------------------------- problem generators


def h_div_missing(d, q, rng):
    k = rng.randrange(3)
    if k == 0:
        return [BOX, "÷", d, "=", q], d * q
    if k == 1:
        return [d * q, "÷", BOX, "=", q], d
    return [d, "×", BOX, "=", d * q], q


def div_facts(rng, n, divisors, lo=1):
    return [h_div(d, q) for d, q in pick(rng, [(d, q) for d in divisors for q in range(lo, 11)], n)]


def sym(x, y):
    return "=" if x == y else (">" if x > y else "<")


# ---------------------------------------------------------------- book assembly
ST = {
    "h1": ParagraphStyle("h1", fontName=B, fontSize=21, leading=26, textColor=TH[4][1], spaceAfter=8),
    "h2": ParagraphStyle("h2", fontName=B, fontSize=14, leading=18, textColor=TH[1][1], spaceBefore=10, spaceAfter=4),
    "body": ParagraphStyle("body", fontName=R, fontSize=10.5, leading=14.5, spaceAfter=5),
    "bul": ParagraphStyle("bul", fontName=R, fontSize=10.5, leading=14.5, leftIndent=14, bulletIndent=2, spaceAfter=3),
    "cell": ParagraphStyle("cell", fontName=R, fontSize=9.5, leading=12),
    "cellb": ParagraphStyle("cellb", fontName=B, fontSize=9.5, leading=12),
    "note": ParagraphStyle("note", fontName=R, fontSize=10, leading=13.5, leftIndent=10, spaceAfter=2),
    "key_h": ParagraphStyle("key_h", fontName=B, fontSize=11, leading=14, textColor=TH[1][1], spaceBefore=8, spaceAfter=2),
    "key": ParagraphStyle("key", fontName=R, fontSize=9, leading=12.5),
}


def P(s, st="body"):
    return Paragraph(s, ST[st])


def bullets(items):
    return [Paragraph(s, ST["bul"], bulletText="•") for s in items]


def table(rows, widths, theme, raw=False):
    data = [[Paragraph(x if raw else esc(x), ST["cellb" if r == 0 or (c_ == 0) else "cell"])
             for c_, x in enumerate(row)] for r, row in enumerate(rows)]
    tb = Table(data, colWidths=widths, repeatRows=1)
    tb.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), theme[0]), ("GRID", (0, 0), (-1, -1), 0.6, theme[1]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    return tb


def key_story():
    s = [P("Answer Key (for grown-ups)", "h1"),
         P("Answers are listed in order, numbered the same way as on each page.")]
    for title, answers in KEY:
        s.append(P(esc(title), "key_h"))
        s.append(P("&nbsp;&nbsp; ".join(f"<b>{i + 1}.</b>&nbsp;{esc(a)}" for i, a in enumerate(answers)), "key"))
    return s


def section_title(title, sub, theme):
    def draw(c, W, H):
        c.setFillColor(theme[0])
        c.roundRect(0, H / 2 - 90, W, 180, 20, stroke=0, fill=1)
        text(c, W / 2, H / 2 + 10, title, 34, B, theme[1], "c")
        text(c, W / 2, H / 2 - 30, sub, 14, R, INK, "c")
    return draw


# ================================================================= build
def on_page(c, doc):
    c.saveState()
    text(c, PAGE_W / 2, 16, f"– {doc.page} –", 8, R, GRAY, "c")
    c.restoreState()


def build_pdf(out, title, story):
    """Lay out `story` on US Letter pages with page numbers and write it to `out`."""
    doc = BaseDocTemplate(out, pagesize=letter, leftMargin=MARGIN, rightMargin=MARGIN, topMargin=MARGIN,
                          bottomMargin=MARGIN, title=title, author="Learn & practice plan")
    doc.addPageTemplates([PageTemplate("p", [Frame(MARGIN, MARGIN, FW, FH, 0, 0, 0, 0)], onPage=on_page)])
    doc.build(story)
    print("wrote", out)
