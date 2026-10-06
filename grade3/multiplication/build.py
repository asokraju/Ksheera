#!/usr/bin/env python3
"""Grade 3 · Multiplication Mastery: a printable 4-week learn-and-practice book.

Run:  python3 build.py   ->  Multiplication_Mastery_Grade3.pdf
Every worksheet uses a fixed random seed, so the answer key always matches.
"""
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from common.printkit import *  # noqa: E402,F401,F403

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Multiplication_Mastery_Grade3.pdf")


# ================================================================= WEEK 1
def day1():
    T = TH[1]
    probs = [(3, 4), (2, 5), (4, 3), (5, 2), (3, 6), (4, 5)]
    KEY.append(("Day 1 · Equal Groups",
                [f"{g} groups of {n} = {g*n}; {g} × {n} = {g*n}" for g, n in probs]
                + ["Draw it: 3 × 5 = 15", "4 × 2 = 8"]))

    def draw(c, W, H):
        y = header(c, W, H, T, "Week 1 · Day 1", "Equal Groups",
                   "Count the groups. Count how many are in EACH group. Then fill in the boxes. "
                   "Remember: × means \"groups of\".")
        cw, ch = W / 2, 138
        for i, (g, n) in enumerate(probs):
            r, k = divmod(i, 2)
            x, top = k * cw, y - r * ch
            card(c, x + 4, top - ch + 8, cw - 8, ch - 10, T)
            text(c, x + 14, top - 20, f"{i + 1}.", 12, B, T[1])
            draw_groups(c, x + 30, top - 50, cw - 50, g, n, T)
            expr(c, x + 18, top - 92, [BOX, "groups of", BOX, "=", BOX], 12, 28)
            expr(c, x + 18, top - 118, [BOX, "×", BOX, "=", BOX], 12, 28)
        y -= 3 * ch + 4
        y = section(c, y, "B", "Draw it!  Draw circles for groups and dots inside.", T)
        bh = y - 34
        for k, (g, n) in enumerate([(3, 5), (4, 2)]):
            x = k * cw
            card(c, x + 4, y - bh, cw - 8, bh, T)
            text(c, x + 14, y - 18, f"Draw {g} groups of {n}", 12, B, T[1])
            expr(c, x + 18, y - bh + 10, [BOX, "×", BOX, "=", BOX], 12, 28)
        footer(c, W, 8)
    return [draw]


def day2():
    T = TH[1]
    rng = random.Random(102)
    adds = [(4, 5), (3, 6), (6, 2), (5, 3), (2, 9), (4, 7)]
    skips = [3, 4, 6, 7, 8, 9]
    shown = {n: {0} | set(rng.sample(range(1, 10), 3)) for n in skips}
    KEY.append(("Day 2 · Adding & Skip Counting",
                [f"{g} × {n} = {g*n}" for g, n in adds]
                + [f"By {n}s: " + ", ".join(str(n * (k + 1)) for k in range(10) if k not in shown[n])
                   for n in skips]))

    def draw(c, W, H):
        y = header(c, W, H, T, "Week 1 · Day 2", "Repeated Adding & Skip Counting",
                   "Multiplication is a shortcut for adding the same number again and again.")
        y = section(c, y, "A", "Add, then write it as multiplication.", T)
        cw, ch = W / 2, 64
        for i, (g, n) in enumerate(adds):
            r, k = divmod(i, 2)
            x, top = k * cw, y - r * ch
            text(c, x, top - 16, f"{i + 1}.", 11, B, T[1])
            toks = []
            for j in range(g):
                toks += [n] + (["+"] if j < g - 1 else [])
            expr(c, x + 20, top - 16, toks + ["=", BOX], 14, 30)
            expr(c, x + 20, top - 44, [BOX, "×", BOX, "=", BOX], 14, 30)
        y -= 3 * ch + 8
        y = section(c, y, "B", "Skip count! Fill in the missing numbers.", T)
        bw = (W - 64) / 10
        for n in skips:
            text(c, 0, y - 20, f"By {n}s", 12, B, T[1])
            for k in range(10):
                x = 64 + k * bw
                c.setStrokeColor(T[1])
                c.setLineWidth(1)
                c.setFillColor(T[0] if k in shown[n] else WHITE)
                c.roundRect(x, y - 30, bw - 5, 28, 5, stroke=1, fill=1)
                if k in shown[n]:
                    text(c, x + (bw - 5) / 2, y - 21, n * (k + 1), 13, B, INK, "c")
            y -= 40
        y -= 4
        tip(c, y, W, T, [("Think:", "How many 4s are in 4 + 4 + 4? Three 4s, so 3 × 4 = 12.")], 11)
        footer(c, W, 6 + sum(10 - len(shown[n]) for n in skips))
    return [draw]


def day3():
    T = TH[1]
    arrays = [(2, 5), (3, 4), (4, 6), (5, 3), (3, 7), (6, 4)]
    KEY.append(("Day 3 · Arrays",
                [f"{r} rows of {k}; {r} × {k} = {r*k}" for r, k in arrays]
                + ["Draw it: 3 × 6 = 18", "4 × 4 = 16"]))

    def draw(c, W, H):
        y = header(c, W, H, T, "Week 1 · Day 3", "Arrays: Rows of Equal Groups",
                   "An array has rows going across →. Every row has the same number. "
                   "Count the rows and how many are in each row.")
        y = section(c, y, "A", "Write the multiplication for each array.", T)
        cw, ch = W / 2, 124
        for i, (rows, cols) in enumerate(arrays):
            r, k = divmod(i, 2)
            x, top = k * cw, y - r * ch
            card(c, x + 4, top - ch + 8, cw - 8, ch - 10, T)
            text(c, x + 14, top - 20, f"{i + 1}.", 12, B, T[1])
            step = 14
            ah = rows * step
            draw_array(c, x + 32, top - 4 - (ch - 10 - ah) / 2, rows, cols, step, T[1])
            tx = x + 140
            expr(c, tx, top - 32, [BOX, "rows"], 11, 24)
            expr(c, tx, top - 60, [BOX, "in each row"], 11, 24)
            expr(c, tx, top - 90, [BOX, "×", BOX, "=", BOX], 11, 24)
        y -= 3 * ch + 6
        y = section(c, y, "B", "Draw an array with dots.", T)
        bh = y - 34
        for k, (rows, cols) in enumerate([(3, 6), (4, 4)]):
            x = k * cw
            card(c, x + 4, y - bh, cw - 8, bh, T)
            text(c, x + 14, y - 18, f"{rows} rows of {cols}", 12, B, T[1])
            expr(c, x + 18, y - bh + 10, [BOX, "×", BOX, "=", BOX], 12, 28)
        footer(c, W, 8)
    return [draw]


def day4():
    T = TH[1]
    turns = [(7, 3), (8, 4), (6, 9), (5, 7), (9, 2), (4, 6), (10, 3), (8, 6)]
    lines = [(4, 3), (5, 4), (3, 7)]
    KEY.append(("Day 4 · Turn-Around Facts & Number Lines",
                ["2 × 5 = 10 and 5 × 2 = 10", "3 × 4 = 12 and 4 × 3 = 12"]
                + [f"{b} × {a} = {a*b}" for a, b in turns]
                + [f"{j} jumps of {s} = {j*s}; {j} × {s} = {j*s}" for j, s in lines]))

    def draw(c, W, H):
        y = header(c, W, H, T, "Week 1 · Day 4", "Turn-Around Facts & Number Lines",
                   "Turn an array sideways and you get the same total. Order doesn't matter!")
        y = section(c, y, "A", "Fill in both facts. What do you notice?", T)
        cw = W / 4
        for k, (rows, cols) in enumerate([(2, 5), (5, 2), (3, 4), (4, 3)]):
            x = k * cw
            draw_array(c, x + (cw - cols * 12) / 2, y - 2, rows, cols, 12, T[1])
            expr(c, x + 14, y - 78, [rows, "×", cols, "=", BOX], 13, 28)
        y -= 96
        y = section(c, y, "B", "Use the fact you know to fill in the turn-around fact.", T)
        cw = W / 2
        for i, (a, b) in enumerate(turns):
            r, k = divmod(i, 2)
            expr(c, k * cw, y - r * 28 - 14, [f"{a} × {b} = {a*b},  so  {b} × {a} =", BOX], 13, 30)
        y -= 4 * 28 + 4
        y = section(c, y, "C", "Number lines: count the jumps and the size of each jump.", T)
        for j, s in lines:
            numberline(c, 12, y - 40, W - 24, 24, j, s, T)
            expr(c, 12, y - 78, [BOX, "jumps of", BOX, "=", BOX], 12, 28)
            expr(c, 300, y - 78, [BOX, "×", BOX, "=", BOX], 12, 28)
            y -= 86
        footer(c, W, 4 + len(turns) + 3)
    return [draw]


def day5():
    T = TH[1]
    rng = random.Random(105)
    probs = pick(rng, pool(lambda a, b: a in (2, 3, 4, 5, 10) and 1 <= b), 30)
    stories = [
        ("Maya has 4 bags. Each bag has 5 marbles. How many marbles does she have?", "4 × 5 = 20 marbles"),
        ("There are 3 rows of chairs with 7 chairs in each row. How many chairs?", "3 × 7 = 21 chairs"),
        ("A spider has 8 legs. How many legs do 2 spiders have?", "2 × 8 = 16 legs"),
    ]
    KEY.append(("Day 5 · Week 1 Review", [a * b for a, b in probs] + [s[1] for s in stories]))

    def draw(c, W, H):
        y = header(c, W, H, T, "Week 1 · Day 5", "Week 1 Review",
                   "Part A is your first Mad Minute — try it in 3 minutes, then finish. "
                   "Part B has no rush. Draw a picture if it helps!")
        y = section(c, y, "A", "Mad Minute: 2s, 3s, 4s, 5s and 10s", T)
        y = vdrill(c, probs, y, W, 6, 66, 19)
        y = section(c, y - 2, "B", "Word problems", T)
        cw = W / 3
        for i, (s, _) in enumerate(stories):
            word_card(c, i * cw + 3, y, cw - 6, y - 32, i + 1, s, T, ("Answer:",))
        footer(c, W, 33, timed=True)
    return [draw]


# ================================================================= WEEK 2
def day6():
    T = TH[2]
    rng = random.Random(106)
    probs = pick(rng, pool(lambda a, b: a in (0, 1, 2, 5, 10) or b in (0, 1, 2, 5, 10)), 40)
    KEY.append(("Day 6 · Easy Facts", [a * b for a, b in probs]))
    rules = [("× 0", "always 0"), ("× 1", "same number"), ("× 2", "double it"),
             ("× 5", "ends in 0 or 5"), ("× 10", "add a 0 at the end")]

    def draw(c, W, H):
        y = header(c, W, H, T, "Week 2 · Day 6", "Easy Facts: 0, 1, 2, 5, 10",
                   "These are your superpower facts! Read the rules, then solve.")
        tw = W / 5
        for i, (a, b) in enumerate(rules):
            card(c, i * tw + 3, y - 58, tw - 6, 56, T, fill=True)
            text(c, i * tw + tw / 2, y - 26, a, 18, B, T[1], "c")
            text(c, i * tw + tw / 2, y - 46, b, 9.5, R, INK, "c")
        y -= 74
        vdrill(c, probs, y, W, 8, 82, 19)
        footer(c, W, 40, timed=True)
    return [draw]


def table_fill(c, y, W, mults, theme):
    """Rows like ×2, ×4, ×8 with a blank box for n = 1..10."""
    cw = (W - 60) / 10
    for k in range(10):
        text(c, 60 + k * cw + cw / 2, y - 14, k + 1, 12, B, theme[1], "c")
    y -= 22
    for m in mults:
        text(c, 4, y - 21, f"× {m}", 15, B, theme[1])
        for k in range(10):
            c.setStrokeColor(theme[1])
            c.setLineWidth(1)
            c.roundRect(60 + k * cw, y - 30, cw - 5, 28, 5, stroke=1, fill=0)
        y -= 36
    return y - 6


def day7():
    T = TH[2]
    rng = random.Random(107)
    probs = pick(rng, pool(lambda a, b: a in (4, 8) and b >= 1), 32)
    KEY.append(("Day 7 · Doubling", [f"×2: {', '.join(str(2*n) for n in range(1, 11))}",
                                     f"×4: {', '.join(str(4*n) for n in range(1, 11))}",
                                     f"×8: {', '.join(str(8*n) for n in range(1, 11))}"]
                + [a * b for a, b in probs]))

    def draw(c, W, H):
        y = header(c, W, H, T, "Week 2 · Day 7", "Doubling: 2s → 4s → 8s")
        y = tip(c, y, W, T, [("Double:", "6 × 2 = 12"),
                             ("Double again:", "6 × 4 = 24"),
                             ("Double again:", "6 × 8 = 48")], 12)
        y = section(c, y, "A", "Fill in the table. Each row doubles the row above it.", T)
        y = table_fill(c, y, W, (2, 4, 8), T)
        y = section(c, y, "B", "Practice 4s and 8s", T)
        vdrill(c, probs, y, W, 8, 74, 19)
        footer(c, W, 62, timed=True)
    return [draw]


def day8():
    T = TH[2]
    rng = random.Random(108)
    probs = pick(rng, pool(lambda a, b: a in (3, 6, 9) and b >= 1), 32)
    KEY.append(("Day 8 · 3s, 6s and 9s", [f"×3: {', '.join(str(3*n) for n in range(1, 11))}",
                                          f"×6: {', '.join(str(6*n) for n in range(1, 11))}",
                                          f"×9: {', '.join(str(9*n) for n in range(1, 11))}"]
                + [a * b for a, b in probs]))

    def draw(c, W, H):
        y = header(c, W, H, T, "Week 2 · Day 8", "The 3s, 6s and 9s")
        y = tip(c, y, W, T, [("×6 is double ×3:", "7 × 3 = 21, so 7 × 6 = 42"),
                             ("×9 is ×10 minus one group:", "9 × 7 = 70 − 7 = 63"),
                             ("9s check:", "the digits of a 9s answer add to 9 (6 + 3 = 9)")], 12)
        y = section(c, y, "A", "Fill in the table.", T)
        y = table_fill(c, y, W, (3, 6, 9), T)
        y = section(c, y, "B", "Practice 3s, 6s and 9s", T)
        vdrill(c, probs, y, W, 8, 74, 19)
        footer(c, W, 62, timed=True)
    return [draw]


def day9():
    T = TH[2]
    rng = random.Random(109)
    parts = [(6, 7), (7, 7), (8, 6), (6, 8), (7, 8), (8, 7), (8, 8), (7, 6)]
    probs = pick(rng, pool(lambda a, b: a in (6, 7, 8) and b in (6, 7, 8, 9)), 16)
    KEY.append(("Day 9 · Break Apart",
                [f"{a} × {b} = {a} × 5 + {a} × {b-5} = {5*a} + {a*(b-5)} = {a*b}" for a, b in parts]
                + [a * b for a, b in probs]))

    def draw(c, W, H):
        y = header(c, W, H, T, "Week 2 · Day 9", "Break Apart Tricky Facts",
                   "Forgot a fact? Break it into two facts you know, then add them.")
        bh = 112
        card(c, 0, y - bh, W, bh, T, fill=True)
        draw_array(c, 16, y - 10, 7, 8, 11.5, T[1], split=5, color2=TH[3][1])
        c.setStrokeColor(INK)
        c.setDash(3, 2)
        c.line(16 + 5 * 11.5, y - 6, 16 + 5 * 11.5, y - 10 - 7 * 11.5 - 4)
        c.setDash()
        text(c, 130, y - 26, "7 × 8 = ?", 16, B)
        text(c, 130, y - 50, "7 × 5 = 35", 14, B, T[1])
        text(c, 250, y - 50, "+   7 × 3 = 21", 14, B, TH[3][1])
        text(c, 130, y - 78, "7 × 8 = 35 + 21 = 56", 16, B)
        text(c, 130, y - 98, "5s are easy, so break off a 5!", 10.5, R, GRAY)
        y -= bh + 10
        y = section(c, y, "A", "Break apart, then add.", T)
        cw, ch = W / 2, 56
        for i, (a, b) in enumerate(parts):
            r, k = divmod(i, 2)
            x, top = k * cw, y - r * ch
            text(c, x, top - 14, f"{i + 1}.", 10, B, T[1])
            expr(c, x + 18, top - 14, [a, "×", b, "=", a, "×", 5, "+", a, "×", BOX], 13, 26)
            expr(c, x + 58, top - 40, ["=", BOX, "+", BOX, "=", BOX], 13, 30)
        y -= 4 * ch + 4
        y = section(c, y, "B", "Practice tricky facts", T)
        vdrill(c, probs, y, W, 8, 78, 19)
        footer(c, W, 8 + 16, timed=True)
    return [draw]


def day10():
    T = TH[2]
    rng = random.Random(110)
    probs = pick(rng, pool(lambda a, b: True), 48)
    KEY.append(("Day 10 · Fill the Chart", ["Check with the Multiplication Chart page in the front of the book."]))
    KEY.append(("Day 10 · Mad Minute (mixed)", [a * b for a, b in probs]))

    def chart(c, W, H):
        y = header(c, W, H, T, "Week 2 · Day 10", "Fill the Multiplication Chart",
                   "Multiply the row number by the column number. Use turn-around facts to save time!")
        cell = 42
        mult_chart(c, (W - 11 * cell) / 2, y - 4, cell, T, filled=False)
        y -= 11 * cell + 24
        write_line(c, 0, y, W, "A pattern I found:")
        write_line(c, 0, y - 28, W)
        footer(c, W, 100)

    mad = vdrill_page(T, "Week 2 · Day 10", "Mad Minute: Mixed Facts", MAD + "   (Day 5 score: ____)",
                      probs, 8, 82, "")
    KEY.pop()
    return [chart, mad]


# ================================================================= WEEK 3
def day11():
    T = TH[3]
    fams = [(4, 6), (3, 7), (5, 8), (6, 9), (2, 9), (7, 8), (4, 7), (6, 8)]
    KEY.append(("Day 11 · Fact Families",
                [f"{a}×{b}={a*b}, {b}×{a}={a*b}, {a*b}÷{a}={b}, {a*b}÷{b}={a}" for a, b in fams]))

    def draw(c, W, H):
        y = header(c, W, H, T, "Week 3 · Day 11", "Fact Families",
                   "Three numbers make four facts: two × facts and two ÷ facts. "
                   "Write all four facts for each triangle.")
        bh = 92
        card(c, 0, y - bh, W, bh, T, fill=True)
        triangle(c, 60, y - bh + 8, 90, 76, 12, 3, 4, T)
        for i, f in enumerate(["3 × 4 = 12", "4 × 3 = 12", "12 ÷ 3 = 4", "12 ÷ 4 = 3"]):
            text(c, 140 + (i // 2) * 150, y - 36 - (i % 2) * 28, f, 15, B)
        text(c, 450, y - 50, "The biggest", 10, R, GRAY, "c")
        text(c, 450, y - 63, "number goes", 10, R, GRAY, "c")
        text(c, 450, y - 76, "first in ÷", 10, R, GRAY, "c")
        y -= bh + 12
        cw, ch = W / 2, 112
        for i, (a, b) in enumerate(fams):
            r, k = divmod(i, 2)
            x, top = k * cw, y - r * ch
            card(c, x + 3, top - ch + 6, cw - 6, ch - 8, T)
            triangle(c, x + 58, top - ch + 20, 90, 76, a * b, a, b, T)
            for j in range(4):
                write_line(c, x + 116, top - 26 - j * 23, x + cw - 14)
        footer(c, W, 32)
    return [draw]


def day12():
    T = TH[3]
    rng = random.Random(112)
    items = [h_miss(a, b, rng) for a, b in pick(rng, pool(lambda a, b: True, 2), 36)]
    KEY.append(("Day 12 · Missing Numbers", [a for _, a in items]))

    def draw(c, W, H):
        y = header(c, W, H, T, "Week 3 · Day 12", "Find the Missing Number")
        y = tip(c, y, W, T, [("6 × ☐ = 42", "Ask: 6 times WHAT makes 42?"),
                             ("Skip count by 6:", "6, 12, 18, 24, 30, 36, 42  →  7 jumps, so ☐ = 7")], 12)
        hdrill(c, [t for t, _ in items], y - 2, W, 3, 39, 16, 30)
        footer(c, W, 36, timed=True)
    return [draw]


def day13():
    T = TH[3]
    rng = random.Random(113)
    pics = [(3, 4), (4, 5), (2, 6), (5, 3)]
    items = [h_div(d, q) for d, q in pick(rng, pool(lambda a, b: a >= 2, 1), 24)]
    KEY.append(("Day 13 · Division", [f"{g*n} ÷ {g} = {n}" for g, n in pics] + [a for _, a in items]))

    def draw(c, W, H):
        y = header(c, W, H, T, "Week 3 · Day 13", "Division: Sharing Equally")
        y = tip(c, y, W, T, [("12 ÷ 3 = 4", "means 12 shared into 3 equal groups gives 4 in each group."),
                             ("To divide, think ×:", "42 ÷ 6 = ?   →   6 × ? = 42   →   7")], 11.5)
        y = section(c, y, "A", "Count all the dots, then count the groups. How many in each group?", T)
        cw, ch = W / 2, 104
        for i, (g, n) in enumerate(pics):
            r, k = divmod(i, 2)
            x, top = k * cw, y - r * ch
            card(c, x + 3, top - ch + 6, cw - 6, ch - 8, T)
            text(c, x + 12, top - 20, f"{i + 1}.", 12, B, T[1])
            draw_groups(c, x + 30, top - 44, cw - 50, g, n, T, 22)
            expr(c, x + 30, top - 86, [BOX, "÷", BOX, "=", BOX], 13, 30)
        y -= 2 * ch + 4
        y = section(c, y, "B", "Divide. Think of the multiplication fact!", T)
        hdrill(c, [t for t, _ in items], y, W, 4, 34, 15, 28)
        footer(c, W, 28, timed=True)
    return [draw]


def day14():
    T = TH[3]
    probs = [
        ("A box holds 6 eggs. How many eggs are in 4 boxes?", "4 × 6 = 24 eggs"),
        ("Leo has 35 stickers. He puts 5 stickers on each page. How many pages does he fill?", "35 ÷ 5 = 7 pages"),
        ("The library has 8 tables. Each table has 4 chairs. How many chairs are there?", "8 × 4 = 32 chairs"),
        ("24 cookies are shared equally among 3 friends. How many cookies does each friend get?", "24 ÷ 3 = 8 cookies"),
        ("A bike has 2 wheels. How many wheels are on 9 bikes?", "9 × 2 = 18 wheels"),
        ("Priya reads 7 pages every day. How many pages does she read in one week (7 days)?", "7 × 7 = 49 pages"),
        ("54 students stand in 6 equal lines. How many students are in each line?", "54 ÷ 6 = 9 students"),
        ("Pencils come in packs of 10. Mr. Diaz needs 60 pencils. How many packs should he buy?", "60 ÷ 10 = 6 packs"),
    ]
    KEY.append(("Day 14 · Word Problems", [a for _, a in probs]))

    def draw(c, W, H):
        y = header(c, W, H, T, "Week 3 · Day 14", "Word Problems: × or ÷ ?")
        y = tip(c, y, W, T, [("Multiply ×", "when you know the number of groups AND how many in each."),
                             ("Divide ÷", "when you know the total and must share or make groups.")], 11.5)
        cw, ch = W / 2, (y - 30) / 4
        for i, (s, _) in enumerate(probs):
            r, k = divmod(i, 2)
            word_card(c, k * cw + 3, y - r * ch, cw - 6, ch - 6, i + 1, s, T)
        footer(c, W, 8)
    return [draw]


def day15():
    T = TH[3]
    rng = random.Random(115)
    items = mixed_items(rng, 18, 15, 12)
    KEY.append(("Day 15 · Week 3 Review (Mad Minute)", [a for _, a in items] + ["Own word problem: check together"]))

    def draw(c, W, H):
        y = header(c, W, H, T, "Week 3 · Day 15", "Week 3 Review: × and ÷", MAD)
        y = hdrill(c, [t for t, _ in items], y - 2, W, 3, 33, 15, 30)
        bh = y - 34
        card(c, 0, y - bh, W, bh, T)
        text(c, 12, y - 18, "Make up your own word problem for a grown-up to solve!", 12, B, T[1])
        footer(c, W, 45, timed=True)
    return [draw]


# ================================================================= WEEK 4
def day16():
    T = TH[4]
    rng = random.Random(116)
    ladders = [(4, 2), (3, 5), (6, 3), (7, 4), (8, 5), (9, 6)]
    tens = []
    for a, b in pick(rng, pool(lambda a, b: True, 2, 9), 24):
        tens.append(([a, "×", b * 10, "=", BOX] if rng.random() < 0.7 else [b * 10, "×", a, "=", BOX], a * b * 10))
    KEY.append(("Day 16 · Multiplying by Tens",
                [f"{a}×{b}={a*b}, {a}×{b*10}={a*b*10}" for a, b in ladders] + [a for _, a in tens]))

    def draw(c, W, H):
        y = header(c, W, H, T, "Week 4 · Day 16", "Multiplying by Tens")
        y = tip(c, y, W, T, [("3 × 4 = 12", "so  3 × 4 tens = 12 tens  →  3 × 40 = 120"),
                             ("Think dimes:", "3 groups of 4 dimes = 12 dimes = 120 cents")], 12)
        y = section(c, y, "A", "Use the small fact to solve the big one.", T)
        cw, ch = W / 3, 76
        for i, (a, b) in enumerate(ladders):
            r, k = divmod(i, 3)
            x, top = k * cw, y - r * ch
            card(c, x + 3, top - ch + 6, cw - 6, ch - 8, T, fill=True)
            expr(c, x + 16, top - 28, [a, "×", b, "=", BOX], 14, 40)
            expr(c, x + 16, top - 58, [a, "×", b * 10, "=", BOX], 14, 40)
        y -= 2 * ch + 4
        y = section(c, y, "B", "Multiply.", T)
        hdrill(c, [t for t, _ in tens], y, W, 3, 36, 15, 42)
        footer(c, W, 36, timed=True)
    return [draw]


def day17():
    T = TH[4]
    rects = [(3, 4), (2, 7), (5, 5), (4, 8), (6, 3), (3, 6)]
    KEY.append(("Day 17 · Area", [f"{r} × {k} = {r*k} square units" for r, k in rects]
                + ["6 × 4 = 24 square feet", "7 × 3 = 21 square meters"]))

    def draw(c, W, H):
        y = header(c, W, H, T, "Week 4 · Day 17", "Area = Rows × Columns",
                   "Area is how many squares cover a shape. Don't count one by one — multiply!")
        y = section(c, y, "A", "Find the area of each rectangle.", T)
        cw, ch = W / 3, 150
        for i, (rows, cols) in enumerate(rects):
            r, k = divmod(i, 3)
            x, top = k * cw, y - r * ch
            card(c, x + 3, top - ch + 6, cw - 6, ch - 8, T)
            text(c, x + 12, top - 18, f"{i + 1}.", 11, B, T[1])
            u = 12
            area_grid(c, x + (cw - cols * u) / 2, top - 12 - (6 - rows) * u / 2, rows, cols, u, T)
            expr(c, x + 14, top - 104, [BOX, "×", BOX, "=", BOX], 12, 26)
            expr(c, x + 14, top - 130, ["Area =", BOX, "sq units"], 11, 28)
        y -= 2 * ch + 6
        y = section(c, y, "B", "Solve.", T)
        stories = ["A rug is 6 feet long and 4 feet wide. What is its area?",
                   "A garden is 7 meters long and 3 meters wide. What is its area?"]
        for k, s in enumerate(stories):
            word_card(c, k * W / 2 + 3, y, W / 2 - 6, 118, k + 1, s, T)
        footer(c, W, 8)
    return [draw]


def day18():
    T = TH[4]
    threes = [(2, 3, 4), (5, 2, 3), (2, 2, 6), (3, 3, 2), (4, 5, 2), (2, 7, 5), (3, 2, 8), (1, 9, 6)]
    comps = [((6, 4), (3, 8)), ((5, 5), (6, 4)), ((7, 3), (4, 6)), ((9, 2), (3, 6)),
             ((8, 7), (9, 6)), ((4, 9), (6, 6)), ((7, 7), (8, 6)), ((5, 8), (6, 7)),
             ((3, 9), (4, 7)), ((2, 10), (4, 5)), ((6, 9), (7, 8)), ((8, 8), (9, 7))]
    qs = [("6 × 7 = 42. Is 42 odd or even?", "even"),
          ("5 × 9 = 45. Is 45 odd or even?", "odd"),
          ("An odd number × an odd number is always ...", "odd"),
          ("Add the digits of 18, 27, 36, 45. What do you get?", "9 every time")]

    def sym(p, q):
        x, y_ = p[0] * p[1], q[0] * q[1]
        return "=" if x == y_ else (">" if x > y_ else "<")
    KEY.append(("Day 18 · Three Numbers, Compare & Patterns",
                [a * b * d for a, b, d in threes]
                + [f"{p[0]}×{p[1]} {sym(p, q)} {q[0]}×{q[1]}" for p, q in comps] + [a for _, a in qs]))

    def draw(c, W, H):
        y = header(c, W, H, T, "Week 4 · Day 18", "Three Numbers, Compare & Patterns")
        y = section(c, y, "A", "Multiply. Tip: do the easiest pair first!", T)
        y = hdrill(c, [[a, "×", b, "×", d, "=", BOX] for a, b, d in threes], y, W, 2, 32, 15, 32)
        y = section(c, y - 4, "B", "Write >, < or = in the circle.", T)
        y = hdrill(c, [[p[0], "×", p[1], CIRC, q[0], "×", q[1]] for p, q in comps], y, W, 2, 33, 15)
        y = section(c, y - 4, "C", "Patterns", T)
        for i, (q, _) in enumerate(qs):
            text(c, 0, y - 14, f"{i + 1}.  {q}", 11.5)
            write_line(c, 395, y - 14, W)
            y -= 28
        footer(c, W, 24)
    return [draw]


def day19():
    T = TH[4]
    probs = [
        ("Sam buys 3 packs of juice boxes. Each pack has 6 juice boxes. He drinks 4. How many are left?",
         "3 × 6 = 18;  18 − 4 = 14 juice boxes"),
        ("Zoe has 5 bags with 4 apples in each bag. Her mom gives her 7 more apples. How many apples does she have now?",
         "5 × 4 = 20;  20 + 7 = 27 apples"),
        ("A class of 28 students makes teams of 4. Each team gets 2 balls. How many balls are needed?",
         "28 ÷ 4 = 7 teams;  7 × 2 = 14 balls"),
        ("Arjun saves $6 every week for 8 weeks. Then he spends $15 on a book. How much money is left?",
         "6 × 8 = 48;  48 − 15 = $33"),
        ("A garden has 4 rows of 9 flowers. A rabbit eats 6 flowers. How many flowers are left?",
         "4 × 9 = 36;  36 − 6 = 30 flowers"),
        ("Grandma puts 45 cookies equally into 5 boxes. Then she adds 3 more cookies to each box. "
         "How many cookies are in each box now?", "45 ÷ 5 = 9;  9 + 3 = 12 cookies"),
    ]
    KEY.append(("Day 19 · Two-Step Word Problems", [a for _, a in probs]))

    def draw(c, W, H):
        y = header(c, W, H, T, "Week 4 · Day 19", "Two-Step Word Problems")
        y = tip(c, y, W, T, [("Ask:", "What do I need to find FIRST?  Solve step 1, then use that answer in step 2."),
                             ("Example:", "4 boxes of 6 crayons, 5 break.  4 × 6 = 24,  24 − 5 = 19 crayons.")], 11)
        cw, ch = W / 2, (y - 30) / 3
        for i, (s, _) in enumerate(probs):
            r, k = divmod(i, 2)
            word_card(c, k * cw + 3, y - r * ch, cw - 6, ch - 6, i + 1, s, T, ("Step 1:", "Step 2:", "Answer:"))
        footer(c, W, 6)
    return [draw]


def day20():
    T = TH["t"]
    rng = random.Random(120)
    facts = mixed_items(rng, 20, 10, 10)
    tens = [(4, 30), (6, 20), (50, 7), (9, 40), (8, 60), (70, 3)]
    comps = [((7, 6), (8, 5)), ((3, 8), (4, 6)), ((9, 4), (6, 7)), ((5, 6), (3, 10))]
    stories = [
        ("A bus has 9 rows with 4 seats in each row. How many seats are on the bus?", "9 × 4 = 36 seats"),
        ("42 crayons are put equally into 7 boxes. How many crayons are in each box?", "42 ÷ 7 = 6 crayons"),
        ("Noah buys 6 packs of cards with 8 cards in each. He gives 10 cards to his sister. How many cards does he have left?",
         "6 × 8 = 48;  48 − 10 = 38 cards"),
        ("A garden is 7 feet long and 5 feet wide. What is its area?", "7 × 5 = 35 square feet"),
    ]

    def sym(p, q):
        x, y_ = p[0] * p[1], q[0] * q[1]
        return "=" if x == y_ else (">" if x > y_ else "<")
    KEY.append(("Day 20 · Final Test",
                [a for _, a in facts] + [f"{a} × {b} = {a*b}" for a, b in tens]
                + [f"{p[0]}×{p[1]} {sym(p, q)} {q[0]}×{q[1]}" for p, q in comps]
                + [a for _, a in stories]
                + ["Area: 4 × 6 = 24 square units", "5×7=35, 7×5=35, 35÷5=7, 35÷7=5",
                   "8 × 7 = 8 × 5 + 8 × 2 = 40 + 16 = 56"]))
    n1 = len(facts) + len(tens) + len(comps)

    def p1(c, W, H):
        y = header(c, W, H, T, "Week 4 · Day 20 · Final Test · Page 1", "Show What You Know!",
                   "Take your time and check your work. You've got this!")
        y = section(c, y, "A", "Facts", T)
        y = hdrill(c, [t for t, _ in facts], y, W, 4, 33, 14, 28)
        y = section(c, y - 4, "B", "Multiplying by tens", T)
        y = hdrill(c, [[a, "×", b, "=", BOX] for a, b in tens], y, W, 3, 34, 15, 40)
        y = section(c, y - 4, "C", "Write >, < or =", T)
        hdrill(c, [[p[0], "×", p[1], CIRC, q[0], "×", q[1]] for p, q in comps], y, W, 2, 34, 15)
        footer(c, W, n1)

    def p2(c, W, H):
        y = header(c, W, H, T, "Week 4 · Day 20 · Final Test · Page 2", "Show What You Know!")
        y = section(c, y, "D", "Word problems", T)
        cw, ch = W / 2, 128
        for i, (s, _) in enumerate(stories):
            r, k = divmod(i, 2)
            word_card(c, k * cw + 3, y - r * ch, cw - 6, ch - 6, i + 1, s, T)
        y -= 2 * ch + 4
        y = section(c, y, "E", "Area and fact family", T)
        ch = 150
        card(c, 3, y - ch, cw - 6, ch, T)
        area_grid(c, 30, y - 16, 4, 6, 14, T)
        expr(c, 14, y - 100, [BOX, "×", BOX, "=", BOX], 12, 26)
        expr(c, 14, y - 128, ["Area =", BOX, "sq units"], 11, 28)
        card(c, cw + 3, y - ch, cw - 6, ch, T)
        triangle(c, cw + 60, y - ch + 30, 90, 76, 35, 5, 7, T)
        for j in range(4):
            write_line(c, cw + 118, y - 30 - j * 26, W - 12)
        y -= ch + 12
        y = section(c, y, "F", "Break apart, then add.", T)
        expr(c, 10, y - 16, [8, "×", 7, "=", 8, "×", 5, "+", 8, "×", BOX, "=", BOX, "+", BOX, "=", BOX], 15, 34)
        footer(c, W, 11)
    return [p1, p2]


# ================================================================= EXTRAS
def extra_practice():
    T = TH["x"]
    pages = []
    tag = "Extra Practice · print as many as you like"
    seeds = iter(range(201, 300))
    for name, cond in [("A", lambda a, b: True), ("B", lambda a, b: True)]:
        probs = pick(random.Random(next(seeds)), pool(cond), 48)
        pages.append(vdrill_page(T, tag, f"Mad Minute {name}: Mixed Facts", MAD, probs, 8, 82,
                                 f"Extra Practice {name} · Mixed Facts"))
    tricky = lambda a, b: 3 <= min(a, b) and max(a, b) <= 9 and (a >= 6 or b >= 6)
    for name in ("C", "D"):
        probs = pick(random.Random(next(seeds)), pool(tricky), 48)
        pages.append(vdrill_page(T, tag, f"Mad Minute {name}: Tricky 6s, 7s, 8s, 9s", MAD, probs, 8, 82,
                                 f"Extra Practice {name} · Tricky Facts"))
    for name in ("E", "F"):
        rng = random.Random(next(seeds))
        items = [h_div(d, q) for d, q in pick(rng, pool(lambda a, b: True, 1), 45)]
        pages.append(hdrill_page(T, tag, f"Mad Minute {name}: Division", MAD, items, 3, 36,
                                 f"Extra Practice {name} · Division", 16, 30))
    rng = random.Random(next(seeds))
    items = [h_miss(a, b, rng) for a, b in pick(rng, pool(lambda a, b: True, 1), 45)]
    pages.append(hdrill_page(T, tag, "Mad Minute G: Missing Numbers", MAD, items, 3, 36,
                             "Extra Practice G · Missing Numbers", 16, 30))
    rng = random.Random(next(seeds))
    items = mixed_items(rng, 15, 12, 12)
    for a, b in pick(rng, pool(lambda a, b: True, 2, 9), 6):
        items.insert(rng.randrange(len(items)), ([a, "×", b * 10, "=", BOX], a * b * 10))
    pages.append(hdrill_page(T, tag, "Mad Minute H: Everything Mixed", MAD, items, 3, 36,
                             "Extra Practice H · Everything Mixed", 16, 36))
    return pages


def hint(a, b):
    if b == 9:
        return f"{a} × 10 − {a} = {10*a} − {a}"
    if b == 8:
        return f"double {a} × 4 = double {4*a}"
    if b == 7:
        return f"{a} × 5 + {a} × 2 = {5*a} + {2*a}"
    if b == 6:
        return f"{a} × 5 + {a} = {5*a} + {a}"
    if b == 4:
        return f"double {a} × 2 = double {2*a}"
    return f"{a} × 2 + {a} = {2*a} + {a}"


def flash_cards():
    T = TH["x"]
    S = [3, 4, 6, 7, 8, 9]
    facts = [(a, b) for i, a in enumerate(S) for b in S[i:]] + [(5, 7), (5, 8), (5, 9)]

    def make(chunk, page_no):
        def draw(c, W, H):
            text(c, 0, H - 22, f"Fold-Over Flash Cards ({page_no} of 2): the tricky facts", 18, B, T[1])
            text(c, 0, H - 40, "✂ Cut on the solid lines. Fold on the dashed line so the question is on the "
                 "front and the answer is on the back.", 10)
            cw, ch = W / 2, (H - 54) / 6
            for i, (a, b) in enumerate(chunk):
                r, k = divmod(i, 2)
                x, top = k * cw, H - 52 - r * ch
                c.setStrokeColor(GRAY)
                c.setLineWidth(0.8)
                c.rect(x, top - ch, cw, ch, stroke=1, fill=0)
                c.setDash(4, 3)
                c.line(x + cw / 2, top - ch + 6, x + cw / 2, top - 6)
                c.setDash()
                text(c, x + cw / 4, top - ch / 2 - 4, f"{a} × {b}", 24, B, INK, "c")
                text(c, x + cw / 4, top - ch / 2 - 26, f"also {b} × {a}" if a != b else "a square fact!", 9, R, GRAY, "c")
                text(c, x + 3 * cw / 4, top - ch / 2 - 2, a * b, 30, B, T[1], "c")
                text(c, x + 3 * cw / 4, top - ch / 2 - 24, hint(a, b), 8.5, R, GRAY, "c")
        return draw
    return [make(facts[:12], 1), make(facts[12:], 2)]


def bingo():
    T = TH["x"]
    rng = random.Random(301)
    by_prod = {}
    for a in range(2, 11):
        for b in range(a, 11):
            by_prod.setdefault(a * b, []).append((a, b))
    prods = rng.sample(sorted(by_prod), 30)
    calls = sorted((rng.choice(by_prod[p]) for p in prods), key=lambda f: f[0] * f[1])

    def draw(c, W, H):
        text(c, 0, H - 22, "Times Table Bingo", 22, B, T[1])
        para(c, 0, H - 40, "A grown-up reads a fact from the calling list and ticks it. Players cover the "
             "answer with a coin or cereal. 5 in a row wins!", W, 10.5)
        size = 48
        for k in range(2):
            x0 = k * (W / 2) + (W / 2 - 5 * size) / 2
            top = H - 72
            text(c, x0 + 2.5 * size, top - 6, f"Board {k + 1}", 13, B, T[1], "c")
            nums = rng.sample(prods, 24)
            nums.insert(12, "FREE")
            for i, n in enumerate(nums):
                r, j = divmod(i, 5)
                c.setStrokeColor(T[1])
                c.setLineWidth(1)
                c.setFillColor(T[0] if n == "FREE" else WHITE)
                c.rect(x0 + j * size, top - 14 - (r + 1) * size, size, size, stroke=1, fill=1)
                text(c, x0 + j * size + size / 2, top - 14 - (r + 1) * size + size / 2 - 6, n,
                     11 if n == "FREE" else 17, B, INK, "c")
        y = H - 72 - 14 - 5 * size - 30
        text(c, 0, y, "Calling list (tick each fact as you call it)", 13, B, T[1])
        y -= 24
        cw = W / 4
        for i, (a, b) in enumerate(calls):
            r, k = divmod(i, 4)
            text(c, k * cw, y - r * 24, f"☐  {a} × {b}", 13)
            text(c, k * cw + 82, y - r * 24, f"({a*b})", 9, R, GRAY)
    return [draw]


def cover(c, W, H):
    T1, T2, T3, T4 = TH[1], TH[2], TH[3], TH[4]
    c.setFillColor(T1[0])
    c.roundRect(0, H - 190, W, 190, 18, stroke=0, fill=1)
    text(c, W / 2, H - 70, "Multiplication", 44, B, T1[1], "c")
    text(c, W / 2, H - 120, "Mastery", 44, B, T4[1], "c")
    text(c, W / 2, H - 160, "A 4-week learn & practice plan for 3rd grade", 15, R, INK, "c")
    cell = 30
    x0, top = (W - 11 * cell) / 2, H - 220
    palette = [T1, T2, T3, T4, TH["x"]]
    for i in range(11):
        for j in range(11):
            th = palette[(i + j) % 5]
            c.setFillColor(th[1] if (i == 0 or j == 0) else th[0])
            c.setStrokeColor(WHITE)
            c.setLineWidth(1.5)
            c.roundRect(x0 + j * cell, top - (i + 1) * cell, cell, cell, 4, stroke=1, fill=1)
            v = "×" if i == j == 0 else (i or j) if (i == 0 or j == 0) else i * j
            text(c, x0 + j * cell + cell / 2, top - (i + 1) * cell + 10, v, 10,
                 B, WHITE if (i == 0 or j == 0) else INK, "c")
    y = top - 11 * cell - 50
    write_line(c, 90, y, W - 90, "This book belongs to:", 15)
    y -= 50
    for k, (wk, name) in enumerate([("Week 1", "What it means"), ("Week 2", "Strategies & speed"),
                                    ("Week 3", "× and ÷ together"), ("Week 4", "Use it!")]):
        th = palette[k]
        x = k * W / 4
        card(c, x + 4, y - 46, W / 4 - 8, 50, th, fill=True)
        text(c, x + W / 8, y - 16, wk, 12, B, th[1], "c")
        text(c, x + W / 8, y - 34, name, 10, R, INK, "c")


def poster(c, W, H):
    tiles = [("× 0", "Zero groups = nothing", "7 × 0 = 0"),
             ("× 1", "One group = same number", "1 × 8 = 8"),
             ("× 2", "Double it", "2 × 7 = 7 + 7 = 14"),
             ("× 3", "Double, then add 1 group", "3 × 6 = 12 + 6 = 18"),
             ("× 4", "Double, then double again", "4 × 7:  14 → 28"),
             ("× 5", "Half of × 10", "5 × 8 = half of 80 = 40"),
             ("× 6", "× 5, then add 1 group", "6 × 7 = 35 + 7 = 42"),
             ("× 7", "× 5 plus × 2", "7 × 8 = 40 + 16 = 56"),
             ("× 8", "Double, double, double", "8 × 6:  12 → 24 → 48"),
             ("× 9", "× 10, then minus 1 group", "9 × 6 = 60 − 6 = 54"),
             ("× 10", "Put a 0 on the end", "10 × 4 = 40"),
             ("Turn it!", "Order doesn't matter", "3 × 8 = 8 × 3 = 24")]
    palette = [TH[1], TH[2], TH[3], TH[4]]
    text(c, W / 2, H - 30, "My Multiplication Strategy Poster", 24, B, TH[4][1], "c")
    text(c, W / 2, H - 50, "Forgot a fact? Don't guess — use a strategy!", 12, R, INK, "c")
    cw, ch = W / 3, 138
    top = H - 66
    for i, (h, rule, ex) in enumerate(tiles):
        r, k = divmod(i, 3)
        th = palette[(r + k) % 4]
        x, y = k * cw, top - r * ch
        card(c, x + 4, y - ch + 6, cw - 8, ch - 8, th, fill=True, radius=12)
        text(c, x + cw / 2, y - 44, h, 28, B, th[1], "c")
        text(c, x + cw / 2, y - 74, rule, 10.5, B, INK, "c")
        text(c, x + cw / 2, y - 100, ex, 12, R, INK, "c")
    y = top - 4 * ch - 4
    card(c, 4, y - 74, W - 8, 72, TH["x"], fill=True, radius=12)
    text(c, 18, y - 24, "9s finger trick", 14, B, TH["x"][1])
    para(c, 18, y - 44, "Hold up 10 fingers. For 9 × 4, fold down finger number 4. Fingers on the left of it = "
         "tens (3). Fingers on the right = ones (6). So 9 × 4 = 36!", W - 40, 11)


def chart_page(c, W, H):
    T = TH[1]
    text(c, W / 2, H - 30, "Multiplication Chart", 26, B, T[1], "c")
    text(c, W / 2, H - 52, "Find the row number and the column number. The answer is where they meet.", 11, R, INK, "c")
    cell = 46
    x0, top = (W - 11 * cell) / 2, H - 70
    mult_chart(c, x0, top, cell, T, filled=True, size=15)
    y = top - 11 * cell - 26
    for line in ["★ The shaded squares (1×1, 2×2, 3×3 ...) are the \"square numbers\".",
                 "★ The chart is a mirror across the shaded line — that's the turn-around rule!",
                 "★ Look down the 5s column: every answer ends in 0 or 5."]:
        text(c, 30, y, line, 11)
        y -= 20


def certificate(c, W, H):
    T = TH[4]
    c.setStrokeColor(T[1])
    c.setLineWidth(6)
    c.roundRect(10, 60, W - 20, H - 120, 20, stroke=1, fill=0)
    c.setLineWidth(1.5)
    c.setStrokeColor(TH[3][1])
    c.roundRect(24, 74, W - 48, H - 148, 14, stroke=1, fill=0)
    text(c, W / 2, H - 150, "★  ★  ★", 34, B, TH[3][1], "c")
    text(c, W / 2, H - 210, "Certificate of", 26, R, INK, "c")
    text(c, W / 2, H - 258, "Multiplication Mastery", 34, B, T[1], "c")
    text(c, W / 2, H - 320, "This certificate is proudly awarded to", 14, R, INK, "c")
    write_line(c, 110, H - 380, W - 110)
    for i, line in enumerate(["for learning what multiplication means, using smart strategies,",
                              "solving division and word problems, and practicing every day!"]):
        text(c, W / 2, H - 425 - i * 20, line, 13, R, INK, "c")
    write_line(c, 70, H - 540, 250)
    write_line(c, W - 250, H - 540, W - 70)
    text(c, 160, H - 558, "Date", 11, R, GRAY, "c")
    text(c, W - 160, H - 558, "Signed", 11, R, GRAY, "c")
    text(c, W / 2, 110, "Great job, superstar!", 16, B, TH[2][1], "c")



# ================================================================= PARENT GUIDE (flowing text)
PLAN = [
    (1, "What does multiplication MEAN?", [
        (1, "Equal groups", "understands × as \"groups of\""),
        (2, "Repeated adding & skip counting", "turns adding into multiplying"),
        (3, "Arrays", "sees rows × columns"),
        (4, "Turn-around facts & number lines", "knows 3 × 7 = 7 × 3; uses jumps"),
        (5, "Review + first Mad Minute", "explains × three ways; sets a starting score")]),
    (2, "Strategies & speed", [
        (6, "Easy facts: ×0, ×1, ×2, ×5, ×10", "uses rules for over half the chart"),
        (7, "Doubling: 2s → 4s → 8s", "builds 4s and 8s from doubles"),
        (8, "3s, 6s and 9s", "×6 = double ×3; ×9 = ×10 minus a group"),
        (9, "Break apart tricky facts", "solves 7 × 8 from 7 × 5 + 7 × 3"),
        (10, "Fill the chart + Mad Minute", "finds patterns; measures progress")]),
    (3, "Multiplication ↔ Division", [
        (11, "Fact families", "3 numbers, 4 facts"),
        (12, "Missing numbers", "solves 6 × ☐ = 42"),
        (13, "Division: sharing equally", "divides by thinking of a × fact"),
        (14, "Word problems: × or ÷?", "chooses the right operation"),
        (15, "Review Mad Minute", "mixed × and ÷ fluency")]),
    (4, "Use it!", [
        (16, "Multiplying by tens", "3 × 40 = 120, and why"),
        (17, "Area", "area = rows × columns"),
        (18, "Three numbers & comparing", "any order; >, <, ="),
        (19, "Two-step word problems", "plans step 1 and step 2"),
        (20, "Final test + certificate", "shows mastery!")]),
]

TEACH = {
    1: ("Put 3 plates on the table with 4 crackers on each. Ask: How many plates (groups)? How many on each "
        "plate? How many in all? Then let her build 4 groups of 2 and 5 groups of 3.",
        "\"3 groups of 4 is 12. We write it 3 × 4 = 12. The × sign means 'groups of'.\"",
        "Groups must be EQUAL. Put 2 crackers on one plate and 5 on another — can we use × here? (No!)"),
    2: ("Write 4 + 4 + 4 + 4 = 16. Ask: how many 4s did we add? (Four.) So it's 4 × 4. Then skip-count by 3s "
        "while clapping, raising one finger per number. Fingers = number of groups.",
        "\"Multiplication is a shortcut for adding the same number again and again.\"",
        "Mixing up the number of groups and the size of each group. Ask: what number repeats, and how many times?"),
    3: ("Show an egg carton (2 rows of 6) or a muffin tin (3 rows of 4). Build arrays with coins: 3 rows of 5. "
        "Rows go across, columns go down.",
        "\"An array is equal groups lined up in rows. 3 rows of 5 is 3 × 5 = 15.\"",
        "Uneven rows. Every row in an array has the same number."),
    4: ("Build a 2 × 5 coin array on a sheet of paper, then turn the paper sideways — now it's 5 rows of 2, "
        "same coins! Then draw a number line from 0 to 20 and make 4 jumps of 5.",
        "\"Order doesn't matter: 3 × 7 = 7 × 3. You only need to learn half the chart!\"",
        "On number lines, count the JUMPS, not the tick marks."),
    5: ("Ask her to teach YOU (or a stuffed toy) what 4 × 6 means three ways: groups, array and number line. "
        "Then Part A is her first Mad Minute — write the score on the tracker. It's just a starting point.",
        "\"Let's see where you start. From now on you only have to beat yourself!\"",
        "Pressure. Keep it light and fun."),
    6: ("Talk through each rule with objects: 5 empty plates = 0 (×0). One plate of 7 = 7 (×1). ×2 = doubles. "
        "×5 = counting nickels or minutes on a clock. ×10 = dimes. Color these rows on the chart — it's over half of it!",
        "\"These are your superpower facts. You'll use them to figure out the harder ones.\"",
        "×0 vs ×1 mix-ups: 6 × 0 = 0, but 6 × 1 = 6."),
    7: ("Show 6 × 2 = 12. Double it: 6 × 4 = 24. Double again: 6 × 8 = 48. Try with 7: 14 → 28 → 56.",
        "\"To multiply by 4, double twice. To multiply by 8, double three times.\"",
        "Doubling 2-digit numbers like 28. Split it: double 20 = 40, double 8 = 16, 40 + 16 = 56."),
    8: ("×6 is double ×3: 7 × 3 = 21, so 7 × 6 = 42. ×9 is ×10 minus one group: 9 × 7 = 70 − 7 = 63. "
        "Show the 9s finger trick from the Strategy Poster.",
        "\"If you know your 3s, you know your 6s. If you know your 10s, you know your 9s!\"",
        "In 9s answers the digits add to 9 (6 + 3) — a quick self-check."),
    9: ("Draw a 7 × 8 array on grid paper. Draw a line after 5 columns. Now it's 7 × 5 (35) and 7 × 3 (21). "
        "Add: 35 + 21 = 56. Try 6 × 7 = 6 × 5 + 6 × 2.",
        "\"When you forget a fact, break it into facts you know, then add.\"",
        "Forgetting to add the two parts at the end."),
    10: ("She fills the whole blank chart. Hunt for patterns together: it's a mirror across the diagonal "
         "(turn-around facts!), the 5s end in 0 or 5, the even rows are all even. Then a Mad Minute — compare with Day 5.",
         "\"Look how much faster you got!\"",
         "Facts that are still slow. Write them on sticky notes for the fridge."),
    11: ("Write 3, 4 and 12 on a triangle. Show the 4 facts: 3 × 4, 4 × 3, 12 ÷ 3, 12 ÷ 4. Cover one corner with "
         "your thumb and ask for the hidden number.",
         "\"Three numbers, four facts — they're a family.\"",
         "In a ÷ fact the biggest number (the product) always comes first."),
    12: ("Write 6 × ☐ = 42. Skip-count by 6 on fingers until she reaches 42 — 7 fingers, so ☐ = 7. "
         "Do a few more out loud.",
         "\"Ask yourself: 6 times WHAT makes 42?\"",
         "Writing the product in the box instead of the missing factor."),
    13: ("Sharing: deal 12 crackers onto 3 plates one at a time → 4 each (12 ÷ 3 = 4). Grouping: put 12 crackers "
         "into bags of 4 → 3 bags (12 ÷ 4 = 3).",
         "\"Division undoes multiplication. For 42 ÷ 6, think: 6 × ? = 42.\"",
         "Reading ÷ backwards. Read 12 ÷ 3 as \"12 shared into 3 equal groups\"."),
    14: ("Read each problem twice. Underline the numbers, circle the question. Know the groups AND how many in "
         "each? Multiply. Know the total and need to share or group? Divide. Draw a quick picture if stuck.",
         "\"Picture the story first, then pick × or ÷.\"",
         "Grabbing the numbers and multiplying. Ask her to retell the story in her own words."),
    15: ("Mixed Mad Minute (×, ÷ and missing numbers). Then she makes up her own word problem for YOU to "
         "solve — kids love checking a grown-up's work!",
         "\"You're a multiplication AND division expert now.\"",
         "÷ facts being slower than × facts is normal; they catch up with practice."),
    16: ("Use dimes: 3 groups of 4 dimes = 12 dimes = 120 cents. So 3 × 40 = 120. Write 3 × 4 = 12, "
         "3 × 4 tens = 12 tens = 120.",
         "\"Multiply the small fact, then remember they were tens.\"",
         "Only saying \"add a zero\". Always also say why: 12 tens is 120."),
    17: ("Cover a book or placemat with square sticky notes (or crackers). Count all the squares. Then count rows "
         "and columns and multiply — same answer, much faster!",
         "\"Area is how many squares cover a shape: rows × columns, in square units.\"",
         "Counting around the edge (that's perimeter) instead of the squares inside."),
    18: ("2 × 3 × 4: multiply in any order — pick an easy pair first (2 × 4 = 8, then 8 × 3 = 24). For comparing, "
         "solve each side first, then choose >, < or =.",
         "\"You can group numbers any way you like when you multiply.\"",
         "Comparing only the first numbers: 6 × 4 vs 5 × 5 — 6 is bigger than 5, but 24 is less than 25!"),
    19: ("4 boxes of 6 crayons; 5 break. How many good crayons? Step 1: 4 × 6 = 24. Step 2: 24 − 5 = 19. "
         "Ask: what do I need to find FIRST?",
         "\"Big problems are just small problems in a row.\"",
         "Stopping after step 1. Re-read the question at the end."),
    20: ("Keep it calm; no timer. She may use strategies but not the chart. Afterwards, celebrate and give her "
         "the certificate! Note any slow facts for extra practice.",
         "\"You worked so hard — let's show what you know!\"",
         "Any section under 80%: redo that week's pages and Extra Practice before moving on."),
}

GAMES = [
    ("Multiplication War", "a deck of cards",
     "Remove the face cards (Ace = 1). Each player flips two cards and multiplies them. The bigger product "
     "wins all four cards. Say the whole fact out loud: \"6 times 7 is 42!\""),
    ("Roll &amp; Multiply", "2 dice + the multiplication chart",
     "Roll two dice and multiply. Color the answer on a chart. First to get 4 in a row wins. "
     "For harder facts, add 4 to each die."),
    ("Times Table Bingo", "the Bingo page in this book",
     "You call a fact from the list, she covers the answer. Switch roles so she does the calling, too."),
    ("Array Hunt", "your home",
     "Find arrays around the house: egg cartons (2 × 6), muffin tins, window panes, chocolate bars, tiles. "
     "Say the fact for each one."),
    ("Skip-Count Ball Toss", "a ball",
     "Toss a ball back and forth. Each catch, say the next number: 7, 14, 21, 28 ... Drop it? Start again!"),
    ("Beat the Grown-Up", "flash cards",
     "You answer facts with a silly handicap (hop on one foot, talk like a robot); she answers normally. "
     "First to 10 correct wins."),
    ("Kitchen &amp; Store Math", "everyday life",
     "\"4 packs of 6 yogurts — how many?\"  \"24 grapes shared by 3 people — how many each?\""),
    ("Fact of the Day", "a sticky note",
     "Write one tricky fact on a sticky note on the fridge. Ask it at breakfast, dinner and bedtime."),
]


def guide_story():
    s = []
    s.append(P("Welcome! How to Use This Plan", "h1"))
    s.append(P("She already knows her times tables 1–10 — a wonderful head start! In 3rd grade the goal is bigger "
               "than memorizing. Children are expected to:"))
    s += bullets(["<b>Understand</b> what multiplication means (equal groups, arrays, number lines).",
                  "<b>Use strategies</b> to work out a fact they forget (doubling, breaking apart, turn-arounds).",
                  "<b>Recall facts quickly</b> (fluency with all facts up to 10 × 10).",
                  "<b>Use multiplication</b> for division, word problems, area and multiplying by tens."])
    s.append(P("This book covers all four in <b>20 short lessons: 4 weeks, 5 days a week, about 20–30 minutes a day.</b> "
               "Each day has a short teaching moment (pages 3–5) and a one-page worksheet."))
    s.append(P("The daily routine", "h2"))
    rows = [["Step", "Time", "What to do"],
            ["1. Warm-up", "3 min", "Skip-count out loud by today's number, or run through 10 flash cards."],
            ["2. Teach", "5–8 min", "Use the \"Teach it\" note for the day. Use real objects!"],
            ["3. Practice", "10–15 min", "Today's worksheet. Sit nearby, but let her try first."],
            ["4. Play", "5 min", "One game from the Games page."],
            ["5. Check", "3 min", "Mark it together with the Answer Key. Fix mistakes. Add a sticker to the tracker."]]
    s.append(table(rows, [80, 65, FW - 145], TH[1]))
    s.append(P("Tips that make it stick", "h2"))
    s += bullets([
        "Use things she can touch: cereal, LEGO bricks, coins, buttons, egg cartons, muffin tins.",
        "Ask <b>\"How did you figure that out?\"</b> more often than \"What's the answer?\"",
        "<b>Mad Minute</b> pages: she only races her OWN last score. Accuracy first — speed comes with practice. "
        "A great goal by the end: 40+ facts correct in 3 minutes.",
        "Mistakes are clues, not failures. Put any missed fact on a sticky note on the fridge.",
        "Short and happy beats long and tired. Stop while she still wants more.",
        "Praise effort and strategies (\"You broke 7 × 8 into 7 × 5 and 7 × 3 — clever!\"), not just right answers.",
        "Weekends: no worksheets. Play a game, or do math while cooking and shopping."])
    s.append(P("Printing", "h2"))
    s += bullets([
        "Print the whole book once, single-sided. Keep the <b>Answer Key</b> (last pages) for yourself.",
        "The <b>Extra Practice</b> pages, the blank chart (Day 10) and the Bingo page can be reprinted as often as you like.",
        "Pin the <b>Strategy Poster</b> and the <b>Multiplication Chart</b> on the wall or fridge.",
        "<b>After the 4 weeks:</b> keep 5 minutes a day (one Extra Practice page or flash cards) for 2–3 more weeks, "
        "then once a week to keep facts fresh."])
    s.append(PageBreak())

    s.append(P("The 4-Week Plan at a Glance", "h1"))
    for wk, theme_name, days in PLAN:
        th = TH[wk]
        rows = [[f"Week {wk}: {theme_name}", "", ""], ["Day", "Lesson", "She will be able to..."]]
        rows += [[str(d), t, g] for d, t, g in days]
        tb = Table([[Paragraph(esc(x) if i else x, ST["cellb" if r < 2 else "cell"]) for i, x in enumerate(row)]
                    for r, row in enumerate(rows)], colWidths=[40, 210, FW - 250])
        tb.setStyle(TableStyle([
            ("SPAN", (0, 0), (-1, 0)), ("BACKGROUND", (0, 0), (-1, 0), th[1]),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE), ("BACKGROUND", (0, 1), (-1, 1), th[0]),
            ("GRID", (0, 0), (-1, -1), 0.6, th[1]), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
        tb._cellvalues[0][0] = Paragraph(f"<font color='white'>Week {wk}: {esc(theme_name)}</font>", ST["cellb"])
        s += [tb, Spacer(1, 10)]
    s.append(P("Every week ends with a review day. If a review shows a weak spot, spend an extra day on it "
               "using the Extra Practice pages — it's fine to go slower. Mastery matters more than the calendar."))
    s.append(PageBreak())

    s.append(P("Teaching Notes: What to Do Each Day", "h1"))
    s.append(P("Spend 5–8 minutes on this before the worksheet. Real objects make it click."))
    titles = {d: t for _, _, days in PLAN for d, t, _ in days}
    for wk, theme_name, days in PLAN:
        s.append(P(f"Week {wk}: {esc(theme_name)}", "h2"))
        for d, _, _ in days:
            teach, say, watch = TEACH[d]
            s.append(KeepTogether([
                P(f"<font color='{TH[wk][1].hexval().replace('0x', '#')}'><b>Day {d} · {esc(titles[d])}</b></font>", "body"),
                P(f"<b>Teach it:</b> {esc(teach)}", "note"),
                P(f"<b>Say:</b> {esc(say)}", "note"),
                P(f"<b>Watch for:</b> {esc(watch)}", "note"),
                Spacer(1, 4)]))
    s.append(PageBreak())

    s.append(P("Games: 5 Minutes of Fun Practice", "h1"))
    s.append(P("Play one game a day after the worksheet, and on weekends instead of worksheets. "
               "Games build speed without stress."))
    rows = [["Game", "You need", "How to play"]] + [[g, n, h] for g, n, h in GAMES]
    s.append(table(rows, [115, 100, FW - 215], TH[2], raw=True))
    s.append(P("Daily warm-up ideas", "h2"))
    s += bullets(["Skip-count forwards and backwards by the day's number.",
                  "\"Quick-fire 10\": ask 10 facts in a row; she answers as fast as she can.",
                  "Flash cards: sort into \"I know it fast\" and \"I need to think\" piles. Practice the second pile."])
    s.append(PageBreak())
    return s


def tracker_story():
    s = [P("My Progress Tracker", "h1"),
         P("After each day, write the date, the score, and add a sticker or draw a star!")]
    titles = [(d, t) for _, _, days in PLAN for d, t, _ in days]
    rows = [["Day", "Lesson", "Date", "Score", "Mad Minute", "★"]]
    rows += [[str(d), t, "", "", "" if d in (5, 10, 15) else "—", ""] for d, t in titles]
    tb = Table([[Paragraph(esc(x), ST["cellb" if r == 0 else "cell"]) for x in row] for r, row in enumerate(rows)],
               colWidths=[34, 220, 74, 66, 82, 64], rowHeights=[None] + [23] * 20)
    style = [("GRID", (0, 0), (-1, -1), 0.6, TH[4][1]), ("BACKGROUND", (0, 0), (-1, 0), TH[4][0]),
             ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]
    for i, (d, _) in enumerate(titles):
        style.append(("BACKGROUND", (0, i + 1), (0, i + 1), TH[(d - 1) // 5 + 1][0]))
    tb.setStyle(TableStyle(style))
    s += [tb, Spacer(1, 14), P("Extra Practice Log", "h2")]
    rows = [["Sheet", "Date", "Score", "Time", "Sheet", "Date", "Score", "Time"]] + [[""] * 8 for _ in range(5)]
    tb = Table(rows, colWidths=[FW / 8] * 8, rowHeights=[18] + [24] * 5)
    tb.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.6, TH["x"][1]), ("BACKGROUND", (0, 0), (-1, 0), TH["x"][0]),
                            ("FONTNAME", (0, 0), (-1, -1), B), ("FONTSIZE", (0, 0), (-1, -1), 9)]))
    s += [tb, PageBreak()]
    return s


def build():
    pages = []
    for d in (day1, day2, day3, day4, day5, day6, day7, day8, day9, day10,
              day11, day12, day13, day14, day15, day16, day17, day18, day19, day20):
        pages += d()
    extras = extra_practice()

    story = [Page(cover)] + guide_story()
    story += [Page(poster), Page(chart_page)] + tracker_story()
    week_names = {1: "What does multiplication mean?", 2: "Strategies & speed",
                  3: "Multiplication ↔ Division", 4: "Use it!"}
    per_week = [5, 6, 5, 6]  # Day 10 and Day 20 have two pages
    i = 0
    for wk in (1, 2, 3, 4):
        story.append(Page(section_title(f"Week {wk}", week_names[wk], TH[wk])))
        story += [Page(f) for f in pages[i:i + per_week[wk - 1]]]
        i += per_week[wk - 1]
    story.append(Page(section_title("Extra Practice", "Reprint these pages as often as you like", TH["x"])))
    story += [Page(f) for f in extras + flash_cards() + bingo()]
    story.append(Page(certificate))
    story += key_story()
    build_pdf(OUT, "Multiplication Mastery – 3rd Grade", story)


if __name__ == "__main__":
    build()
