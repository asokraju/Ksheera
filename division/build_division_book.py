#!/usr/bin/env python3
"""Build a printable 3rd-grade division book: one hands-on lesson for today + practice until it's easy.

Run:  python3 build_division_book.py   ->  Division_Made_Easy_Grade3.pdf
Reuses the drawing helpers from ../multiplication/build_book.py. Fixed seeds keep the answer key in sync.
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "multiplication"))
from build_book import (B, BOX, CIRC, FH, FW, GRAY, INK, KEY, MAD, MARGIN, R, ST, TH, WHITE, P, Page,  # noqa: E402
                        bullets, card, colors, esc, expr, footer, h_mul, hdrill, hdrill_page, header, mult_chart,
                        numberline, on_page, para, pick, pool, section, stringWidth, table, text, tip, triangle,
                        word_card, write_line)
from reportlab.lib.pagesizes import letter  # noqa: E402
from reportlab.platypus import (BaseDocTemplate, Frame, KeepTogether, PageBreak, PageTemplate,  # noqa: E402
                                Spacer, Table, TableStyle)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Division_Made_Easy_Grade3.pdf")
COOKIE, CHIP = colors.HexColor("#F3D9A4"), colors.HexColor("#8A5A1E")


# ---------------------------------------------------------------- pictures
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
def h_div(d, q):
    return [d * q, "÷", d, "=", BOX], q


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


# ================================================================= TODAY'S LESSON
L = "Today's Lesson · Part"


def lesson1():
    T = TH[3]
    probs = [(12, 3), (10, 2), (15, 5), (8, 4), (18, 3), (20, 4)]
    KEY.append(("Part 1 · Fair Sharing", [f"{n} ÷ {g} = {n // g} (each plate gets {n // g})" for n, g in probs]))

    def draw(c, W, H):
        y = header(c, W, H, T, f"{L} 1", "Fair Sharing",
                   "Share the cookies so every plate gets the SAME number. Cross out a cookie at the top, "
                   "then draw it on a plate. Go round and round until all cookies are shared!")
        y = tip(c, y, W, T, [("12 ÷ 3 = 4", "means: 12 shared equally onto 3 plates gives 4 on each plate.")], 11.5)
        cw, ch = W / 2, 150
        for i, (n, g) in enumerate(probs):
            r, k = divmod(i, 2)
            x, top = k * cw, y - r * ch
            card(c, x + 3, top - ch + 6, cw - 6, ch - 8, T)
            text(c, x + 12, top - 20, f"{i + 1}.", 12, B, T[1])
            text(c, x + 30, top - 20, f"Share {n} cookies on {g} plates.", 11.5, B)
            cookie_rows(c, x + 30, top - 30, n)
            slot = (cw - 50) / g
            pr = min(25, slot * 0.42)
            for j in range(g):
                plate(c, x + 25 + slot * (j + 0.5), top - 92, pr)
            expr(c, x + 14, top - 136, [n, "÷", g, "=", BOX, "  Each plate gets", BOX], 12, 28)
        footer(c, W, 6)
    return draw


def lesson2():
    T = TH[2]
    rng = random.Random(402)
    probs = [(12, 4), (15, 3), (18, 6), (20, 5), (14, 2), (16, 4)]
    KEY.append(("Part 2 · Making Groups", [f"{n // s} groups; {n} ÷ {s} = {n // s}" for n, s in probs]))

    def draw(c, W, H):
        y = header(c, W, H, T, f"{L} 2", "Making Equal Groups",
                   "Circle groups of stars. Every group must have the same number. "
                   "Then count how many groups you made!")
        y = tip(c, y, W, T, [("12 ÷ 4 = 3", "means: 12 stars put in groups of 4 makes 3 groups.")], 11.5)
        cw, ch = W / 2, 150
        for i, (n, s) in enumerate(probs):
            r, k = divmod(i, 2)
            x, top = k * cw, y - r * ch
            card(c, x + 3, top - ch + 6, cw - 6, ch - 8, T)
            text(c, x + 12, top - 20, f"{i + 1}.", 12, B, T[1])
            text(c, x + 30, top - 20, f"Circle groups of {s}.", 11.5, B)
            scattered_stars(c, x + 14, top - 32, n, rng, T[1], cols=5 if s in (2, 4, 6) and n % 5 else 6)
            expr(c, x + 158, top - 56, [BOX, "groups"], 12, 28)
            expr(c, x + 158, top - 96, [n, "÷", s, "=", BOX], 12, 28)
        footer(c, W, 6)
    return draw


def lesson3():
    T = TH[1]
    arrays = [(3, 5), (2, 7), (4, 4), (5, 3), (3, 6), (4, 6)]
    KEY.append(("Part 3 · Arrays", [f"{r * k} ÷ {r} = {k}; {r} × {k} = {r * k}" for r, k in arrays]))

    def draw(c, W, H):
        y = header(c, W, H, T, f"{L} 3", "Arrays Show × and ÷",
                   "Count how many dots are in ONE row. That is the answer to the division!")
        bh = 92
        card(c, 0, y - bh, W, bh, T, fill=True)
        from build_book import draw_array
        draw_array(c, 18, y - 14, 3, 4, 16, T[1])
        for i, f in enumerate(["3 rows of 4:   3 × 4 = 12", "12 dots in 3 rows:   12 ÷ 3 = 4",
                               "12 dots in rows of 4:   12 ÷ 4 = 3"]):
            text(c, 110, y - 26 - i * 24, f, 13, B, INK)
        text(c, W - 14, y - 82, "Same picture, × and ÷ !", 10, R, GRAY, "r")
        y -= bh + 12
        cw, ch = W / 2, 150
        for i, (rows, cols) in enumerate(arrays):
            r, k = divmod(i, 2)
            x, top = k * cw, y - r * ch
            card(c, x + 3, top - ch + 6, cw - 6, ch - 8, T)
            text(c, x + 12, top - 20, f"{i + 1}.", 12, B, T[1])
            text(c, x + 30, top - 20, f"{rows * cols} dots in {rows} equal rows", 11.5, B)
            draw_array(c, x + 26, top - 32, rows, cols, 14, T[1])
            expr(c, x + 140, top - 60, [rows * cols, "÷", rows, "=", BOX], 13, 28)
            expr(c, x + 140, top - 98, [rows, "×", BOX, "=", rows * cols], 13, 28)
        footer(c, W, 12)
    return draw


def lesson4():
    T = TH[4]
    rng = random.Random(404)
    pairs = pick(rng, [(d, q) for d in range(2, 10) for q in range(2, 10)], 12)
    fams = [(3, 5), (4, 7), (6, 8), (2, 9)]
    KEY.append(("Part 4 · Think Multiplication",
                [f"{q} and {q}" for d, q in pairs]
                + [f"{a}×{b}={a*b}, {b}×{a}={a*b}, {a*b}÷{a}={b}, {a*b}÷{b}={a}" for a, b in fams]))

    def draw(c, W, H):
        y = header(c, W, H, T, f"{L} 4", "The Shortcut: Think Multiplication!")
        y = tip(c, y, W, T, [("24 ÷ 6 = ?", "Ask yourself:  6 times WHAT makes 24?"),
                             ("6 × 4 = 24,", "so  24 ÷ 6 = 4.   You already know this from your times tables!")], 12)
        y = section(c, y, "A", "Fill in the multiplication, then the division.", T)
        cw = W / 2
        for i, (d, q) in enumerate(pairs):
            r, k = divmod(i, 2)
            expr(c, k * cw, y - r * 36 - 14, [d, "×", BOX, "=", d * q, "  so ", d * q, "÷", d, "=", BOX], 13, 26)
        y -= 6 * 36 + 6
        y = section(c, y, "B", "Fact families: write 2 × facts and 2 ÷ facts.", T)
        ch = (y - 30) / 2
        for i, (a, b) in enumerate(fams):
            r, k = divmod(i, 2)
            x, top = k * cw, y - r * ch
            card(c, x + 3, top - ch + 6, cw - 6, ch - 8, T)
            triangle(c, x + 58, top - ch + 20, 90, 76, a * b, a, b, T)
            for j in range(4):
                write_line(c, x + 116, top - 26 - j * 23, x + cw - 14)
        footer(c, W, 28)
    return draw


def lesson5():
    T = TH["x"]
    shown = [(20, 5), (18, 3)]
    blank = [(24, 6), (16, 4)]
    subs = [(15, 5), (12, 4), (14, 7), (18, 6)]
    KEY.append(("Part 5 · Jump Back (optional)",
                [f"{n // s} jumps; {n} ÷ {s} = {n // s}" for n, s in shown + blank]
                + [f"{n // s} times; {n} ÷ {s} = {n // s}" for n, s in subs]))

    def draw(c, W, H):
        y = header(c, W, H, T, f"{L} 5 (another way)", "Jump Back to Zero",
                   "Start at the total. Jump back by the same size until you land on 0. "
                   "The number of jumps is the answer!")
        y = section(c, y, "A", "Count the jumps.", T)
        for n, s in shown:
            jumps_back(c, 12, y - 40, W - 24, 24, n, s, T)
            expr(c, 12, y - 76, [BOX, f"jumps of {s}, so", n, "÷", s, "=", BOX], 12, 28)
            y -= 88
        y = section(c, y, "B", "Draw the jumps yourself.", T)
        for n, s in blank:
            text(c, 12, y - 12, f"Start at {n}. Jump back by {s}s.", 11, B, T[1])
            jumps_back(c, 12, y - 46, W - 24, 24, 0, s, T)
            expr(c, 300, y - 12, [n, "÷", s, "=", BOX], 12, 28)
            y -= 70
        y = section(c, y, "C", "Take away the same number again and again.", T)
        for n, s in subs:
            toks = [n] + sum([["−", s] for _ in range(n // s)], []) + ["= 0"]
            x = expr(c, 0, y - 14, toks, 12)
            expr(c, max(x + 10, 250), y - 14, ["I took away", s, BOX, "times.", n, "÷", s, "=", BOX], 12, 26)
            y -= 30
        footer(c, W, 12)
    return draw


def lesson6():
    T = TH[3]
    probs = [
        ("15 strawberries are shared equally by 3 friends. How many does each friend get?", "15 ÷ 3 = 5 strawberries"),
        ("There are 20 socks. How many pairs (groups of 2) can you make?", "20 ÷ 2 = 10 pairs"),
        ("18 crayons go equally into 6 boxes. How many crayons are in each box?", "18 ÷ 6 = 3 crayons"),
        ("24 kids make teams of 4. How many teams are there?", "24 ÷ 4 = 6 teams"),
        ("30 cupcakes are put equally on 5 plates. How many cupcakes are on each plate?", "30 ÷ 5 = 6 cupcakes"),
        ("Mom has 16 stickers. She gives 4 stickers to each kid. How many kids get stickers?", "16 ÷ 4 = 4 kids"),
        ("A week has 7 days. How many weeks are in 28 days?", "28 ÷ 7 = 4 weeks"),
        ("36 marbles are put equally into 9 bags. How many marbles are in each bag?", "36 ÷ 9 = 4 marbles"),
    ]
    KEY.append(("Part 6 · Word Problems", [a for _, a in probs]))

    def draw(c, W, H):
        y = header(c, W, H, T, f"{L} 6", "Division Stories")
        y = tip(c, y, W, T, [("Find the TOTAL first.", "Then: do you know the number of groups, or how many in each?"),
                             ("Total ÷ groups", "= how many in each group.     Total ÷ how many in each = groups.")], 11)
        cw, ch = W / 2, (y - 30) / 4
        for i, (s, _) in enumerate(probs):
            r, k = divmod(i, 2)
            word_card(c, k * cw + 3, y - r * ch, cw - 6, ch - 6, i + 1, s, T)
        footer(c, W, 8)
    return draw


# ================================================================= PRACTICE (after today)
def helper_strip(c, y, W, divisors, theme):
    """Times-table helper rows, e.g. '× 2:  2 4 6 ...'."""
    h = 18 * len(divisors) + 26
    card(c, 0, y - h, W, h, theme, fill=True)
    text(c, 10, y - 15, "Helper (cover it with a sticky note when you're ready!)", 9.5, B, theme[1])
    for i, d in enumerate(divisors):
        yy = y - 33 - i * 18
        text(c, 10, yy, f"× {d}:", 11, B, theme[1])
        for k in range(10):
            text(c, 70 + k * 46, yy, d * (k + 1), 11, R, INK, "c")
    return y - h - 8


def practice_facts(n, T, title, divisors, seed, stories):
    rng = random.Random(seed)
    items = div_facts(rng, 33, divisors)
    KEY.append((f"Practice {n} · {title}", [a for _, a in items] + [a for _, a in stories]))

    def draw(c, W, H):
        y = header(c, W, H, T, f"Practice · Day {n}", title)
        y = helper_strip(c, y, W, divisors, T)
        y = section(c, y, "A", "Divide. Think: what times the small number makes the big one?", T)
        y = hdrill(c, [t for t, _ in items], y, W, 3, 33, 15, 28)
        y = section(c, y - 2, "B", "Quick stories", T)
        for i, (s, _) in enumerate(stories):
            text(c, 0, y - 12, f"{i + 1}.  {s}", 11)
            write_line(c, 430, y - 12, W)
            y -= 26
        footer(c, W, 33 + len(stories), timed=True)
    return draw


def practice5():
    T = TH[1]
    rng = random.Random(505)
    base = [(1, q) for q in range(1, 11)] + [(d, 1) for d in range(1, 11)] + [(10, q) for q in range(1, 11)]
    items = [h_div(d, q) for d, q in pick(rng, base, 26)]
    items += [([0, "÷", d, "=", BOX], 0) for d in rng.sample(range(1, 11), 4)]
    items += [h_div(d, q) for d, q in pick(rng, [(d, q) for d in (2, 5) for q in range(1, 11)], 6)]
    rng.shuffle(items)
    KEY.append(("Practice 5 · Special Rules", [a for _, a in items]))
    tiles = [("÷ 1", "same number", "8 ÷ 1 = 8"), ("n ÷ n", "always 1", "7 ÷ 7 = 1"),
             ("0 ÷ n", "always 0", "0 ÷ 5 = 0"), ("÷ 10", "take off the 0", "60 ÷ 10 = 6")]

    def draw(c, W, H):
        y = header(c, W, H, T, "Practice · Day 5", "Super-Easy Rules: ÷1, ÷10, 0 and Same",
                   "Learn these 4 rules and lots of facts become easy! "
                   "(And never divide BY 0 — you can't share into zero groups.)")
        tw = W / 4
        for i, (a, b, e) in enumerate(tiles):
            card(c, i * tw + 3, y - 74, tw - 6, 72, T, fill=True)
            text(c, i * tw + tw / 2, y - 26, a, 18, B, T[1], "c")
            text(c, i * tw + tw / 2, y - 46, b, 10, B, INK, "c")
            text(c, i * tw + tw / 2, y - 64, e, 10, R, INK, "c")
        y -= 88
        hdrill(c, [t for t, _ in items], y, W, 3, 36, 15, 28)
        footer(c, W, len(items), timed=True)
    return draw


def practice6():
    T = TH[2]
    rng = random.Random(506)
    items = [h_div_missing(d, q, rng) for d, q in pick(rng, [(d, q) for d in range(2, 10) for q in range(2, 10)], 36)]
    KEY.append(("Practice 6 · Missing Numbers", [a for _, a in items]))

    def draw(c, W, H):
        y = header(c, W, H, T, "Practice · Day 6", "Mystery Numbers")
        y = tip(c, y, W, T, [("☐ ÷ 4 = 6", "The box is the TOTAL. 4 groups of 6 → 4 × 6 = 24."),
                             ("24 ÷ ☐ = 6", "How many groups of 6 make 24? → 4."),
                             ("4 × ☐ = 24", "4 times what makes 24? → 6.")], 11.5)
        hdrill(c, [t for t, _ in items], y - 2, W, 3, 38, 16, 30)
        footer(c, W, 36, timed=True)
    return draw


def practice7():
    T = TH[3]
    fams = [(2, 8), (3, 9), (4, 8), (5, 6), (6, 7), (7, 9), (8, 9), (6, 6)]
    KEY.append(("Practice 7 · Fact Families",
                [f"{a}×{b}={a*b}, {b}×{a}={a*b}, {a*b}÷{a}={b}, {a*b}÷{b}={a}" if a != b
                 else f"{a}×{a}={a*a}, {a*a}÷{a}={a} (a square number: only 2 facts!)" for a, b in fams]))

    def draw(c, W, H):
        y = header(c, W, H, T, "Practice · Day 7", "Fact Family Triangles",
                   "Write all the facts for each family: two × facts and two ÷ facts. "
                   "Tip: cover a corner with your thumb — the other two numbers tell you the hidden one!")
        cw, ch = W / 2, (y - 30) / 4
        for i, (a, b) in enumerate(fams):
            r, k = divmod(i, 2)
            x, top = k * cw, y - r * ch
            card(c, x + 3, top - ch + 6, cw - 6, ch - 8, T)
            triangle(c, x + 58, top - ch + 20, 90, 76, a * b, a, b, T)
            for j in range(4):
                write_line(c, x + 116, top - 26 - j * 23, x + cw - 14)
        footer(c, W, 30)
    return draw


def practice8():
    T = TH[4]
    probs = [
        ("40 apples are packed equally into 8 baskets. How many apples are in each basket?", "40 ÷ 8 = 5 apples"),
        ("45 chairs are set up in rows of 9. How many rows are there?", "45 ÷ 9 = 5 rows"),
        ("A book has 63 pages. Lily reads 7 pages a day. How many days will it take?", "63 ÷ 7 = 9 days"),
        ("Dogs have 4 legs. Mia counts 32 dog legs at the park. How many dogs are there?", "32 ÷ 4 = 8 dogs"),
        ("56 cards are dealt equally to 8 players. How many cards does each player get?", "56 ÷ 8 = 7 cards"),
        ("Juice boxes come in packs of 6. The class needs 42. How many packs should they buy?", "42 ÷ 6 = 7 packs"),
        ("★ Challenge: Ana has 20 stickers and Ben has 16. They put them together and share them "
         "equally among 4 friends. How many does each friend get?", "20 + 16 = 36;  36 ÷ 4 = 9 stickers"),
        ("★ Challenge: Dad buys 3 packs of 8 pencils. He shares them equally among 6 kids. "
         "How many pencils does each kid get?", "3 × 8 = 24;  24 ÷ 6 = 4 pencils"),
    ]
    KEY.append(("Practice 8 · Word Problems", [a for _, a in probs]))

    def draw(c, W, H):
        y = header(c, W, H, T, "Practice · Day 8", "More Division Stories",
                   "Draw a quick picture if you get stuck: circles for groups, dots for things.")
        cw, ch = W / 2, (y - 30) / 4
        for i, (s, _) in enumerate(probs):
            r, k = divmod(i, 2)
            word_card(c, k * cw + 3, y - r * ch, cw - 6, ch - 6, i + 1, s, T)
        footer(c, W, 8)
    return draw


def practice9():
    T = TH[1]
    rng = random.Random(509)
    items = [h_mul(a, b) for a, b in pick(rng, pool(lambda a, b: True, 1), 15)]
    items += [h_div(d, q) for d, q in pick(rng, pool(lambda a, b: True, 1), 21)]
    rng.shuffle(items)
    comps = []
    for _ in range(6):
        d1, q1, d2, q2 = rng.randint(2, 9), rng.randint(2, 9), rng.randint(2, 9), rng.randint(2, 9)
        comps.append(((d1 * q1, d1, q1), (d2 * q2, d2, q2)))
    KEY.append(("Practice 9 · × and ÷ Mixed", [a for _, a in items]
                + [f"{p[0]}÷{p[1]} {sym(p[2], q[2])} {q[0]}÷{q[1]}" for p, q in comps]))

    def draw(c, W, H):
        y = header(c, W, H, T, "Practice · Day 9", "× and ÷ Mixed Up!",
                   "Look carefully at each sign before you answer!")
        y = section(c, y, "A", "Solve.", T)
        y = hdrill(c, [t for t, _ in items], y, W, 3, 32, 15, 28)
        y = section(c, y - 4, "B", "Write >, < or = in the circle.", T)
        hdrill(c, [[p[0], "÷", p[1], CIRC, q[0], "÷", q[1]] for p, q in comps], y, W, 2, 34, 15)
        footer(c, W, 42, timed=True)
    return draw


def practice10():
    T = TH["t"]
    rng = random.Random(510)
    facts = div_facts(rng, 24, range(2, 10))
    facts += [h_div_missing(d, q, rng) for d, q in pick(rng, [(d, q) for d in range(2, 10) for q in range(2, 10)], 6)]
    rng.shuffle(facts)
    stories = [("27 students ride in 3 vans equally. How many students are in each van?", "27 ÷ 3 = 9 students"),
               ("A carton holds 10 eggs. How many cartons do you need for 70 eggs?", "70 ÷ 10 = 7 cartons")]
    KEY.append(("Practice 10 · Final Check", [a for _, a in facts] + [a for _, a in stories]
                + ["6×8=48, 8×6=48, 48÷6=8, 48÷8=6"]))

    def draw(c, W, H):
        y = header(c, W, H, T, "Practice · Day 10", "Division Final Check",
                   "No timer. Show what you know — then get your certificate!")
        y = section(c, y, "A", "Facts", T)
        y = hdrill(c, [t for t, _ in facts], y, W, 3, 33, 15, 28)
        y = section(c, y - 4, "B", "Stories and a fact family", T)
        cw = W / 3
        bh = y - 34
        for i, (s, _) in enumerate(stories):
            word_card(c, i * cw + 3, y, cw - 6, bh, i + 1, s, T, ("Sentence:", "Answer:"))
        card(c, 2 * cw + 3, y - bh, cw - 6, bh, T)
        triangle(c, 2 * cw + cw / 2, y - 88, 84, 72, 48, 6, 8, T)
        for j in range(4):
            write_line(c, 2 * cw + 14, y - 106 - j * 18, W - 12)
        footer(c, W, 33)
    return draw


def mad_minutes():
    T = TH["x"]
    tag = "Extra Practice · print as many as you like"
    pages = []
    specs = [("A", "÷ 2, 3, 4, 5", range(2, 6)), ("B", "÷ 6, 7, 8, 9", range(6, 10)),
             ("C", "All Division Facts", range(1, 11)), ("D", "All Division Facts", range(1, 11))]
    for i, (name, title, divs) in enumerate(specs):
        items = div_facts(random.Random(601 + i), 45, divs)
        pages.append(hdrill_page(T, tag, f"Mad Minute {name}: {title}", MAD, items, 3, 36,
                                 f"Mad Minute {name} · {title}", 16, 30))
    rng = random.Random(611)
    items = [h_div_missing(d, q, rng) for d, q in pick(rng, [(d, q) for d in range(1, 11) for q in range(1, 11)], 45)]
    pages.append(hdrill_page(T, tag, "Mad Minute E: Mystery Numbers", MAD, items, 3, 36,
                             "Mad Minute E · Mystery Numbers", 16, 34))
    rng = random.Random(612)
    items = [h_mul(a, b) for a, b in pick(rng, pool(lambda a, b: True, 1), 20)] + div_facts(rng, 25, range(1, 11))
    rng.shuffle(items)
    pages.append(hdrill_page(T, tag, "Mad Minute F: × and ÷ Mixed", MAD, items, 3, 36,
                             "Mad Minute F · × and ÷ Mixed", 16, 34))
    return pages


def flash_cards():
    T = TH["x"]
    facts = [(42, 6), (42, 7), (48, 6), (48, 8), (54, 6), (54, 9), (56, 7), (56, 8), (63, 7), (63, 9),
             (72, 8), (72, 9), (64, 8), (49, 7), (81, 9), (36, 6), (36, 4), (32, 4), (28, 4), (27, 3),
             (24, 3), (45, 5), (35, 7), (24, 6)]

    def make(chunk, page_no):
        def draw(c, W, H):
            text(c, 0, H - 22, f"Division Flash Cards ({page_no} of 2)", 18, B, T[1])
            text(c, 0, H - 40, "✂ Cut on the solid lines. Fold on the dashed line: question on the front, "
                 "answer on the back.", 10)
            cw, ch = W / 2, (H - 54) / 6
            for i, (n, d) in enumerate(chunk):
                r, k = divmod(i, 2)
                x, top = k * cw, H - 52 - r * ch
                c.setStrokeColor(GRAY)
                c.setLineWidth(0.8)
                c.rect(x, top - ch, cw, ch, stroke=1, fill=0)
                c.setDash(4, 3)
                c.line(x + cw / 2, top - ch + 6, x + cw / 2, top - 6)
                c.setDash()
                text(c, x + cw / 4, top - ch / 2 - 4, f"{n} ÷ {d}", 24, B, INK, "c")
                text(c, x + cw / 4, top - ch / 2 - 26, f"Think: {d} × ? = {n}", 9, R, GRAY, "c")
                text(c, x + 3 * cw / 4, top - ch / 2 - 2, n // d, 30, B, T[1], "c")
                text(c, x + 3 * cw / 4, top - ch / 2 - 24, f"because {d} × {n // d} = {n}", 9, R, GRAY, "c")
        return draw
    return [make(facts[:12], 1), make(facts[12:], 2)]


# ================================================================= kid reference pages
def cover(c, W, H):
    T = TH[3]
    c.setFillColor(T[0])
    c.roundRect(0, H - 190, W, 190, 18, stroke=0, fill=1)
    text(c, W / 2, H - 75, "Division", 48, B, T[1], "c")
    text(c, W / 2, H - 122, "Made Easy", 40, B, TH[4][1], "c")
    text(c, W / 2, H - 162, "Learn it today, then practice until it's easy · 3rd grade", 14, R, INK, "c")
    # 12 cookies being shared onto 3 plates
    y = H - 260
    cookie_rows(c, W / 2 - 89, y, 12, r=6.5, gap=15, per_row=12)
    for j in range(3):
        cx = W / 2 + (j - 1) * 150
        plate(c, cx, y - 110, 52)
        for k in range(4):
            cookie(c, cx + (k % 2 - 0.5) * 30, y - 110 + (k // 2 - 0.5) * 30, 11)
    arrow(c, W / 2, y - 26, W / 2, y - 48, TH[3][1], 2)
    text(c, W / 2, y - 200, "12 ÷ 3 = 4", 40, B, INK, "c")
    text(c, W / 2, y - 228, "12 cookies shared equally on 3 plates = 4 on each plate", 13, R, INK, "c")
    write_line(c, 90, y - 300, W - 90, "This book belongs to:", 15)
    for k, (wk, name) in enumerate([("Today", "Learn it (6 parts)"), ("Next 10 days", "Practice pages"),
                                    ("Anytime", "Mad Minutes & cards")]):
        th = [TH[3], TH[2], TH["x"]][k]
        x = k * W / 3
        card(c, x + 4, y - 400, W / 3 - 8, 50, th, fill=True)
        text(c, x + W / 6, y - 370, wk, 12, B, th[1], "c")
        text(c, x + W / 6, y - 388, name, 10, R, INK, "c")


def poster(c, W, H):
    text(c, W / 2, H - 30, "What Does ÷ Mean?", 26, B, TH[3][1], "c")
    text(c, W / 2, H - 52, "Division is fair sharing. Everyone gets the SAME amount.", 12, R, INK, "c")
    top = H - 66
    ph = 190
    panels = [
        (TH[3], "1. SHARING", "How many in EACH group?", "12 cookies, 3 plates", "12 ÷ 3 = 4 on each plate"),
        (TH[2], "2. GROUPING", "How many GROUPS?", "12 cookies, 4 in each bag", "12 ÷ 4 = 3 bags"),
    ]
    for k, (th, h1, h2, l1, l2) in enumerate(panels):
        x = k * W / 2
        card(c, x + 4, top - ph, W / 2 - 8, ph, th, fill=True, radius=12)
        text(c, x + W / 4, top - 26, h1, 16, B, th[1], "c")
        text(c, x + W / 4, top - 44, h2, 11, B, INK, "c")
        if k == 0:
            for j in range(3):
                cx = x + W / 4 + (j - 1) * 76
                plate(c, cx, top - 92, 30)
                for m in range(4):
                    cookie(c, cx + (m % 2 - 0.5) * 18, top - 92 + (m // 2 - 0.5) * 18, 7)
        else:
            for j in range(3):
                cx = x + W / 4 + (j - 1) * 76
                c.setStrokeColor(th[1])
                c.setFillColor(WHITE)
                c.setLineWidth(1.4)
                c.roundRect(cx - 28, top - 122, 56, 58, 8, stroke=1, fill=1)
                for m in range(4):
                    cookie(c, cx + (m % 2 - 0.5) * 18, top - 93 + (m // 2 - 0.5) * 18, 7)
        text(c, x + W / 4, top - 150, l1, 11, R, INK, "c")
        text(c, x + W / 4, top - 174, l2, 15, B, INK, "c")
    y = top - ph - 12
    th = TH[4]
    card(c, 4, y - 130, W - 8, 130, th, fill=True, radius=12)
    text(c, W / 2, y - 28, "3. THE SHORTCUT: multiplication backwards!", 16, B, th[1], "c")
    text(c, W / 2, y - 62, "42 ÷ 6 = ?     →     6 × ? = 42     →     6 × 7 = 42", 17, B, INK, "c")
    text(c, W / 2, y - 92, "So 42 ÷ 6 = 7", 20, B, th[1], "c")
    text(c, W / 2, y - 116, "You know your times tables, so you already know every division answer!", 11, R, INK, "c")
    y -= 144
    th = TH[1]
    card(c, 4, y - 112, W - 8, 112, th, fill=True, radius=12)
    text(c, W / 2, y - 24, "How to read it", 15, B, th[1], "c")
    text(c, W / 2, y - 56, "12  ÷  3  =  4", 26, B, INK, "c")
    labels = [(-108, "total"), (-36, "groups"), (68, "in each")]
    for dx, lab in labels:
        text(c, W / 2 + dx, y - 78, lab, 10, B, th[1], "c")
    text(c, W / 2, y - 100, "Say it: \"12 shared into 3 groups is 4 each.\"   The total always goes FIRST.", 11, R, INK, "c")
    y -= 126
    tiles = [("÷ 1", "8 ÷ 1 = 8"), ("n ÷ n", "7 ÷ 7 = 1"), ("0 ÷ n", "0 ÷ 5 = 0"), ("÷ 10", "60 ÷ 10 = 6")]
    tw = W / 4
    for i, (a, b) in enumerate(tiles):
        th = [TH[2], TH[3], TH[4], TH["x"]][i]
        card(c, i * tw + 4, y - 64, tw - 8, 64, th, fill=True, radius=10)
        text(c, i * tw + tw / 2, y - 28, a, 18, B, th[1], "c")
        text(c, i * tw + tw / 2, y - 50, b, 11, R, INK, "c")


def chart_page(c, W, H):
    T = TH[1]
    text(c, W / 2, H - 30, "Use Your Times Table Backwards", 24, B, T[1], "c")
    text(c, W / 2, H - 52, "Every multiplication chart is also a division chart!", 12, R, INK, "c")
    cell = 44
    x0, top = (W - 11 * cell) / 2, H - 66
    mult_chart(c, x0, top, cell, T, filled=True, size=14)
    hi = TH[3][1]
    c.setStrokeColor(hi)
    c.setLineWidth(3)
    for (i, j) in ((6, 0), (6, 7), (0, 7)):
        c.rect(x0 + j * cell, top - (i + 1) * cell, cell, cell, stroke=1, fill=0)
    ry = top - 6.5 * cell
    arrow(c, x0 + cell, ry, x0 + 7 * cell - 4, ry, hi)
    arrow(c, x0 + 7.5 * cell, top - 6 * cell, x0 + 7.5 * cell, top - cell - 4, hi)
    y = top - 11 * cell - 28
    text(c, 20, y, "Example: 42 ÷ 6 = ?", 15, B, hi)
    for i, s in enumerate(["1.  Find 6 in the left column (the number you divide by).",
                           "2.  Slide across that row until you find 42 (the total).",
                           "3.  Go straight up to the top row. You land on 7.   So 42 ÷ 6 = 7!"]):
        text(c, 20, y - 24 - i * 20, s, 12)


def certificate(c, W, H):
    T = TH[3]
    c.setStrokeColor(T[1])
    c.setLineWidth(6)
    c.roundRect(10, 60, W - 20, H - 120, 20, stroke=1, fill=0)
    c.setLineWidth(1.5)
    c.setStrokeColor(TH[4][1])
    c.roundRect(24, 74, W - 48, H - 148, 14, stroke=1, fill=0)
    text(c, W / 2, H - 150, "★  ★  ★", 34, B, TH[4][1], "c")
    text(c, W / 2, H - 210, "Certificate of", 26, R, INK, "c")
    text(c, W / 2, H - 258, "Division Mastery", 38, B, T[1], "c")
    text(c, W / 2, H - 320, "This certificate is proudly awarded to", 14, R, INK, "c")
    write_line(c, 110, H - 380, W - 110)
    for i, line in enumerate(["for learning to share fairly, make equal groups,",
                              "and use multiplication to divide like a pro!"]):
        text(c, W / 2, H - 425 - i * 20, line, 13, R, INK, "c")
    write_line(c, 70, H - 540, 250)
    write_line(c, W - 250, H - 540, W - 70)
    text(c, 160, H - 558, "Date", 11, R, GRAY, "c")
    text(c, W - 160, H - 558, "Signed", 11, R, GRAY, "c")
    text(c, W / 2, 110, "You did it, superstar!", 16, B, TH[2][1], "c")


def section_title(title, sub, theme):
    def draw(c, W, H):
        c.setFillColor(theme[0])
        c.roundRect(0, H / 2 - 90, W, 180, 20, stroke=0, fill=1)
        text(c, W / 2, H / 2 + 10, title, 34, B, theme[1], "c")
        text(c, W / 2, H / 2 - 30, sub, 14, R, INK, "c")
    return draw


# ================================================================= parent guide
PARTS = [
    ("Part 1 · Fair sharing", "15 min", "Page: Part 1",
     "Put 12 crackers and 3 plates on the table. Say: \"Let's share these FAIRLY so every plate gets the same.\" "
     "Let her deal them one at a time — one on each plate, round and round — until they're gone. Count: 4 on each.",
     "\"We started with 12, shared them equally onto 3 plates, and each plate got 4. We write that 12 ÷ 3 = 4. "
     "The ÷ sign means 'shared equally into'.\"",
     "Try 10 crackers on 2 plates, then 15 on 5 plates. Each time ask: \"Is it fair? Does every plate have the same?\"",
     "Unequal plates. Division is always FAIR sharing — every group the same."),
    ("Part 2 · Making groups", "15 min", "Page: Part 2",
     "Same 12 crackers. Now say: \"Each bag gets 4 crackers. How many bags can we fill?\" She makes piles of 4 "
     "and finds 3 bags.",
     "\"This is ALSO division! 12 ÷ 4 = 3. This time we knew how many go in each group, and found how many groups.\"",
     "\"Did you notice? Part 1 used 12, 3 and 4. Part 2 used 12, 4 and 3. The same three numbers!\"",
     "Don't worry about the words 'sharing' and 'grouping'. Both are just ÷."),
    ("Break", "5–10 min", "", "Snack time — she can eat the crackers she shared!", "", "", ""),
    ("Part 3 · Arrays", "10 min", "Page: Part 3",
     "Make 3 rows of 4 coins. \"How many? 3 × 4 = 12. Now: 12 coins in 3 rows — how many in each row? 12 ÷ 3 = 4. "
     "12 coins in rows of 4 — how many rows? 12 ÷ 4 = 3.\"",
     "\"Same picture, multiplication AND division. They're a team.\"",
     "Point at one row: \"The division answer is how many are in one row.\"",
     "Counting all the dots instead of one row."),
    ("Part 4 · The shortcut", "15 min", "Page: Part 4  (the most important part!)",
     "Write 24 ÷ 6 = ?. \"Instead of sharing 24 crackers, let's use your times tables. Ask: 6 times WHAT makes 24?\" "
     "She knows 6 × 4 = 24, so 24 ÷ 6 = 4. Do 10 out loud: 20 ÷ 5, 18 ÷ 3, 35 ÷ 7, 16 ÷ 2, 27 ÷ 9, 30 ÷ 6, "
     "40 ÷ 8, 21 ÷ 7, 36 ÷ 4, 50 ÷ 10.",
     "\"You already know ALL the division answers, because you know your times tables. "
     "Division is multiplication backwards!\"",
     "At first, have her say the whole thing: \"42 ÷ 6 = 7, because 6 × 7 = 42.\"",
     "Putting the numbers in the wrong order (3 ÷ 12). The total always goes first."),
    ("Part 5 · Jump back (optional)", "10 min", "Page: Part 5",
     "Only if she likes number lines or needs another way to see it: start at 20, hop back by 5s to 0 and count the hops.",
     "\"How many 5s fit into 20? Four hops, so 20 ÷ 5 = 4.\"", "", ""),
    ("Part 6 · Division stories", "15 min", "Page: Part 6",
     "Read each story together. Act it out with crackers or draw circles (groups) and dots (things).",
     "\"Total ÷ groups = how many in each. Total ÷ how many in each = how many groups.\"",
     "\"What's the total? Do we know the number of groups, or how many go in each?\"",
     "Grabbing two numbers without thinking. Ask her to retell the story in her own words first."),
]

PRACTICE_PLAN = [
    ("1", "÷ 2, 3", "Practice Day 1"), ("2", "÷ 4, 5", "Practice Day 2"), ("3", "÷ 6, 7", "Practice Day 3"),
    ("4", "÷ 8, 9", "Practice Day 4"), ("5", "Easy rules: ÷1, ÷10, 0, same", "Practice Day 5"),
    ("6", "Mystery numbers", "Practice Day 6"), ("7", "Fact families", "Practice Day 7"),
    ("8", "Word problems", "Practice Day 8"), ("9", "× and ÷ mixed", "Practice Day 9"),
    ("10", "Final check + certificate", "Practice Day 10"),
]

GAMES = [
    ("Snack Share", "snacks + plates or cups",
     "Hand her a pile (e.g. 18 grapes) and a number of plates. She shares fairly, then says the fact: \"18 ÷ 3 = 6\"."),
    ("Division War", "a deck of cards (no face cards)",
     "Flip two cards and multiply secretly (e.g. 6 and 7 → 42). Show only ONE card and say the product: "
     "\"42, and I have a 6. What's my hidden card?\" She answers 42 ÷ 6 = 7."),
    ("Party Planner", "paper",
     "\"We have 30 balloons for 5 friends. How many each?\" \"36 kids at the party, tables of 6. How many tables?\" "
     "Let her make up some for you, too."),
    ("Fact Triangle Thumb", "the fact triangles",
     "Cover one corner of a triangle with your thumb. She names the hidden number and says a ÷ fact."),
]


def guide_story():
    s = [P("Today's Lesson: Division in One Afternoon", "h1")]
    s.append(P("<b>Good news:</b> she already knows her times tables, so she already knows the answer to every "
               "division fact. She just needs to SEE that division is fair sharing, and that it's "
               "multiplication backwards. Today goes from <b>real snacks → pictures → numbers</b>."))
    s.append(P("Get ready (2 minutes)", "h2"))
    s += bullets(["About 20–30 small snacks (crackers, cereal, grapes) or LEGO bricks / coins.",
                  "4–5 small plates or paper cups, and a few zip bags.",
                  "This book, a pencil, and the <b>What Does ÷ Mean?</b> poster on the table."])
    s.append(P("The plan (about 75 minutes with a break)", "h2"))
    rows = [["Part", "Time", "Worksheet"]] + [[p[0], p[1], p[2]] for p in PARTS]
    s.append(table(rows, [190, 70, FW - 260], TH[3]))
    s.append(Spacer(1, 6))
    s.append(P("You don't have to finish everything today. <b>Parts 1, 2 and 4 are the heart of it.</b> If she is "
               "tired, stop after Part 4 and do Part 6 tomorrow. End on a win, while she still feels smart."))
    s.append(P("How you'll know it clicked", "h2"))
    s += bullets(["She can share 15 snacks onto 3 plates and say \"15 ÷ 3 = 5\".",
                  "She can say 24 ÷ 6 = 4 <i>because</i> 6 × 4 = 24.",
                  "She can explain 12 ÷ 3 to a toy or sibling in her own words. Teaching it back is the best test!"])
    s.append(P("Common mix-ups", "h2"))
    s += bullets([
        "<b>12 ÷ 3 vs 3 ÷ 12:</b> the total (the biggest number) always comes first.",
        "<b>Leftovers:</b> if she shares 13 crackers on 3 plates, 1 is left over. That's called a remainder and comes "
        "in 4th grade. Every problem in this book shares evenly.",
        "<b>Dividing by 0:</b> you can't share into zero groups, so it isn't allowed. But 0 ÷ 5 = 0 (nothing to share)."])
    s.append(PageBreak())

    s.append(P("What to Do and Say in Each Part", "h1"))
    for name, time, page, do, say, ask, watch in PARTS:
        if not say:
            continue
        col = TH[3][1].hexval().replace("0x", "#")
        items = [P(f"<font color='{col}'><b>{esc(name)}</b></font>  ({esc(time)}{' · ' + esc(page) if page else ''})", "body"),
                 P(f"<b>Do:</b> {esc(do)}", "note"), P(f"<b>Say:</b> {esc(say)}", "note")]
        if ask:
            items.append(P(f"<b>Ask:</b> {esc(ask)}", "note"))
        if watch:
            items.append(P(f"<b>Watch for:</b> {esc(watch)}", "note"))
        s.append(KeepTogether(items + [Spacer(1, 5)]))
    s.append(P("<b>Wrap-up:</b> celebrate! Ask her to teach a toy what 12 ÷ 3 means using the crackers. "
               "Pin the poster on the fridge.", "body"))
    s.append(PageBreak())

    s.append(P("After Today: Practice Until It's Easy", "h1"))
    s.append(P("Understanding happens today. <b>Speed and confidence come from a little practice every day.</b> "
               "Plan on about 15–20 minutes a day for 10 days."))
    rows = [["Day", "Focus", "Do this"]] + [[d, f, f"{p}, then flash cards or a game"] for d, f, p in PRACTICE_PLAN]
    s.append(table(rows, [40, 190, FW - 230], TH[2]))
    s.append(P("Practice as much as she needs", "h2"))
    s += bullets([
        "<b>Score 90% or more?</b> Move on to the next day.",
        "<b>Under 90%?</b> Stay on that topic. Do a Mad Minute sheet that matches it (A: ÷2–5, B: ÷6–9, "
        "C/D: all facts, E: mystery numbers, F: × and ÷ mixed), then try again. Reprint as often as you like.",
        "Practice Days 1–4 have a <b>helper strip</b> of times tables. Let her use it, then cover it with a sticky note "
        "once she feels ready.",
        "Missed facts go on the fridge as sticky notes: \"42 ÷ 6 = 7 because 6 × 7 = 42\".",
        "<b>Goal by the end:</b> 35–40 division facts correct in 3 minutes. Accuracy first, speed later.",
        "<b>Keep it going:</b> after the 10 days, one Mad Minute twice a week keeps it fresh."])
    s.append(P("Quick games (5 minutes)", "h2"))
    s.append(table([["Game", "You need", "How to play"]] + [list(g) for g in GAMES], [100, 110, FW - 210], TH[4]))
    s.append(PageBreak())
    return s


def tracker_story():
    s = [P("My Division Tracker", "h1"), P("Write the date and score, and add a sticker or a star!")]
    rows = [["", "Page", "Date", "Score", "★"]]
    rows += [[f"Today", f"Part {i}", "", "", ""] for i in range(1, 7)]
    rows += [[f"Day {d}", f, "", "", ""] for d, f, _ in PRACTICE_PLAN]
    tb = Table(rows, colWidths=[60, 230, 90, 90, 70], rowHeights=[20] + [22] * 16)
    style = [("GRID", (0, 0), (-1, -1), 0.6, TH[3][1]), ("BACKGROUND", (0, 0), (-1, 0), TH[3][0]),
             ("FONTNAME", (0, 0), (-1, -1), R), ("FONTNAME", (0, 0), (-1, 0), B), ("FONTSIZE", (0, 0), (-1, -1), 9.5),
             ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("BACKGROUND", (0, 1), (0, 6), TH[3][0]),
             ("BACKGROUND", (0, 7), (0, 16), TH[2][0])]
    tb.setStyle(TableStyle(style))
    s += [tb, Spacer(1, 12), P("Mad Minute Log", "h2")]
    rows = [["Sheet", "Date", "Score", "Time", "Sheet", "Date", "Score", "Time"]] + [[""] * 8 for _ in range(7)]
    tb = Table(rows, colWidths=[FW / 8] * 8, rowHeights=[18] + [23] * 7)
    tb.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.6, TH["x"][1]), ("BACKGROUND", (0, 0), (-1, 0), TH["x"][0]),
                            ("FONTNAME", (0, 0), (-1, -1), B), ("FONTSIZE", (0, 0), (-1, -1), 9)]))
    s += [tb, PageBreak()]
    return s


def key_story():
    s = [P("Answer Key (for grown-ups)", "h1"), P("Answers are listed in the same order as on each page.")]
    for title, answers in KEY:
        s.append(P(esc(title), "key_h"))
        s.append(P("&nbsp;&nbsp; ".join(f"<b>{i + 1}.</b>&nbsp;{esc(a)}" for i, a in enumerate(answers)), "key"))
    return s


def build():
    doc = BaseDocTemplate(OUT, pagesize=letter, leftMargin=MARGIN, rightMargin=MARGIN, topMargin=MARGIN,
                          bottomMargin=MARGIN, title="Division Made Easy – 3rd Grade", author="Learn & practice plan")
    doc.addPageTemplates([PageTemplate("p", [Frame(MARGIN, MARGIN, FW, FH, 0, 0, 0, 0)], onPage=on_page)])

    lessons = [lesson1(), lesson2(), lesson3(), lesson4(), lesson5(), lesson6()]
    practice = [
        practice_facts(1, TH[1], "Divide by 2 and 3", (2, 3), 501,
                       [("14 cookies shared by 2 kids. How many each?", "7"),
                        ("21 flowers in 3 equal vases. How many in each vase?", "7"),
                        ("How many groups of 3 are in 18?", "6")]),
        practice_facts(2, TH[2], "Divide by 4 and 5", (4, 5), 502,
                       [("35 cents in nickels (5¢ each). How many nickels?", "7"),
                        ("28 wheels. How many cars (4 wheels each)?", "7"),
                        ("40 pencils shared by 5 kids. How many each?", "8")]),
        practice_facts(3, TH[3], "Divide by 6 and 7", (6, 7), 503,
                       [("42 days. How many weeks (7 days each)?", "6"),
                        ("48 eggs, 6 eggs in each box. How many boxes?", "8"),
                        ("49 beads shared by 7 friends. How many each?", "7")]),
        practice_facts(4, TH[4], "Divide by 8 and 9", (8, 9), 504,
                       [("A spider has 8 legs. 64 legs is how many spiders?", "8"),
                        ("81 chairs in 9 equal rows. How many in each row?", "9"),
                        ("72 crayons, 8 in a box. How many boxes?", "9")]),
        practice5(), practice6(), practice7(), practice8(), practice9(), practice10(),
    ]
    extras = mad_minutes()

    story = [Page(cover)] + guide_story() + [Page(poster), Page(chart_page)] + tracker_story()
    story.append(Page(section_title("Today's Lesson", "Learn what division means — 6 short parts", TH[3])))
    story += [Page(f) for f in lessons]
    story.append(Page(section_title("Practice", "10 days · about 15–20 minutes a day", TH[2])))
    story += [Page(f) for f in practice]
    story.append(Page(section_title("Extra Practice", "Reprint these pages as often as she needs", TH["x"])))
    story += [Page(f) for f in extras + flash_cards()]
    story.append(Page(certificate))
    story += key_story()
    doc.build(story)
    print("wrote", OUT)


if __name__ == "__main__":
    build()
