#!/usr/bin/env python3
"""Kindergarten · Rudhra's Word Workshop: reading 3-letter (CVC) words, themed around circuits, trains,
cars and the school bus. 4 weeks × 5 short days, parent guide, games, cut-outs and a certificate.

Run:  python3 build.py   ->  Rudhras_Word_Workshop_3_Letter_Words.pdf
"""
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from common.printkit import *  # noqa: E402,F401,F403
from common.icons import ICONS, LBLU as ICON_LBLU, YEL as ICON_YEL  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Rudhras_Word_Workshop_3_Letter_Words.pdf")
NAME = "Rudhra"
VOWELS = "aeiou"
LGRAY = colors.HexColor("#C4C8CE")
WIRE = [colors.HexColor("#E5484D"), colors.HexColor("#2b2b2b"), colors.HexColor("#4C9BE8"),
        colors.HexColor("#4CAF50"), colors.HexColor("#F79A3E"), colors.HexColor("#9B6BD6")]


# ---------------------------------------------------------------- kindergarten page parts
def pic(c, name, x, y, s, frame=None):
    """Picture centered at (x, y) in an s × s box, optionally in a rounded frame."""
    if frame:
        card(c, x - s / 2, y - s / 2, s, s, frame, radius=10)
    ICONS[name](c, x, y, s * (0.82 if frame else 1))


def star_outline(c, cx, cy, r, color=INK):
    p = c.beginPath()
    for i in range(10):
        ang = math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        (p.moveTo if i == 0 else p.lineTo)(cx + rr * math.cos(ang), cy + rr * math.sin(ang))
    p.close()
    c.setStrokeColor(color)
    c.setLineWidth(1.4)
    c.setFillColor(WHITE)
    c.drawPath(p, stroke=1, fill=1)


def tile(c, x, y, w, h, ch, theme, size=None, trace=False, blank=False, fill=WHITE):
    """Letter tile with its lower-left corner at (x, y). Vowels are red; trace letters are light gray."""
    c.setStrokeColor(theme[1])
    c.setLineWidth(1.6)
    c.setFillColor(fill)
    c.roundRect(x, y, w, h, 7, stroke=1, fill=1)
    if blank or not ch:
        return
    size = size or h * 0.68
    col = LGRAY if trace else (TH["t"][1] if ch in VOWELS else INK)
    text(c, x + w / 2, y + h / 2 - size * 0.33, ch, size, R, col, "c")


def k_header(c, W, H, theme, tag, title, grownup=None, icon_name=None):
    light, dark = theme
    c.setLineWidth(1.6)
    c.setStrokeColor(dark)
    c.setFillColor(light)
    c.roundRect(0, H - 66, W, 66, 12, stroke=1, fill=1)
    text(c, 16, H - 20, f"{NAME.upper()}'S WORD WORKSHOP · {tag.upper()}", 9.5, B, dark)
    text(c, 16, H - 52, title, 25, B)
    if icon_name:
        ICONS[icon_name](c, W - 42, H - 33, 54)
    y = H - 86
    if grownup:
        text(c, 0, y, "Grown-up:", 10.5, B, dark)
        y = para(c, 64, y, grownup, W - 64, 10.5, leading=14)
    return y - 4


def k_footer(c, W):
    c.setStrokeColor(GRAY)
    c.setLineWidth(0.6)
    c.line(0, 28, W, 28)
    text(c, 0, 9, f"{NAME}, color a star for each thing you did!", 11, B)
    for i in range(3):
        star_outline(c, 285 + i * 26, 14, 10)
    text(c, W, 9, "Grown-up check  ☐", 11, B, align="r")


def wire(c, pts, color, lw=4):
    """A smooth 'wire' through a list of points."""
    c.setStrokeColor(color)
    c.setLineWidth(lw)
    c.setLineCap(1)
    p = c.beginPath()
    p.moveTo(*pts[0])
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        mx = (x0 + x1) / 2
        p.curveTo(mx, y0, mx, y1, x1, y1)
    c.drawPath(p, stroke=1, fill=0)
    c.setLineCap(0)


def plug(c, x, y, color):
    c.setFillColor(color)
    c.setStrokeColor(INK)
    c.setLineWidth(1)
    c.circle(x, y, 6, stroke=1, fill=1)


# ---------------------------------------------------------------- activity pages
def listen_circle(day, theme, rows, tag):
    KEY.append((f"Day {day} · Robot Ears", [f"{'-'.join(t)} → {t}" for t, _ in rows]))

    def draw(c, W, H):
        y = k_header(c, W, H, theme, tag, "Robot Ears: Listen & Circle",
                     "Say each robot word slowly from the box at the bottom (\"c-a-t\"). Rudhra says the "
                     "word fast (\"cat!\") and circles the picture.", "engine")
        box_h = 54
        rh = (y - 34 - box_h - 10) / len(rows)
        for i, (target, opts) in enumerate(rows):
            top = y - i * rh
            text(c, 14, top - rh / 2 - 8, f"{i + 1}", 26, B, theme[1], "c")
            for k, name in enumerate(opts):
                pic(c, name, 110 + k * 170, top - rh / 2, rh - 14, theme)
        by = 34
        card(c, 0, by, W, box_h, theme, fill=True)
        text(c, 12, by + box_h - 18, "Grown-up reads (robot voice):", 10.5, B, theme[1])
        text(c, 12, by + 12, "     ".join(f"{i + 1}.  {'-'.join(t)}" for i, (t, _) in enumerate(rows)), 15, B)
        k_footer(c, W)
    return draw


def power_bulb(day, theme, items, tag):
    KEY.append((f"Day {day} · Power the Bulb", [w for w, _ in items]))
    rng = random.Random(day)

    def draw(c, W, H):
        y = k_header(c, W, H, theme, tag, "Power the Bulb!",
                     "Rudhra touches each plug and says its SOUND, slides his finger along the wire, then says the "
                     "word fast to light the bulb. He colors the bulb yellow and circles the matching picture.",
                     "bulb")
        rh = (y - 36) / len(items)
        for i, (word, other) in enumerate(items):
            top = y - i * rh
            cy = top - rh / 2
            col = WIRE[i % len(WIRE)]
            xs = [18 + k * 62 for k in range(3)]
            for k, ch in enumerate(word):
                tile(c, xs[k], cy - 8, 52, 50, ch, theme)
            pts = [(x + 26, cy - 20) for x in xs] + [(258, cy - 20)]
            wire(c, pts, col)
            for x, yy in pts[:3]:
                plug(c, x, yy, col)
            ICONS["bulb"](c, 262, cy + 6, 62)
            opts = [word, other]
            rng.shuffle(opts)
            for k, name in enumerate(opts):
                pic(c, name, 380 + k * 112, cy, min(rh - 12, 92), theme)
        k_footer(c, W)
    return draw


def train(c, x, y, letters, theme, trace=True, car_w=66):
    """Engine at x, then 3 cars carrying letters; y = rail height."""
    ICONS["engine"](c, x + 34, y + 30, 68)
    for k, ch in enumerate(letters):
        cx = x + 74 + k * (car_w + 8)
        c.setStrokeColor(GRAY)
        c.setLineWidth(3)
        c.line(cx - 8, y + 10, cx, y + 10)
        tile(c, cx, y + 6, car_w, 56, ch, theme, 40, trace=trace)
        for wx in (cx + 14, cx + car_w - 14):
            c.setFillColor(INK)
            c.circle(wx, y + 4, 7, stroke=0, fill=1)
            c.setFillColor(GRAY)
            c.circle(wx, y + 4, 3, stroke=0, fill=1)
    c.setStrokeColor(GRAY)
    c.setLineWidth(2)
    end = x + 74 + 3 * (car_w + 8)
    c.line(x - 4, y - 4, end, y - 4)


def word_train(day, theme, words, tag):
    KEY.append((f"Day {day} · Load the Train", words))

    def draw(c, W, H):
        y = k_header(c, W, H, theme, tag, "Load the Word Train",
                     "Rudhra names the picture, traces each gray letter while saying its sound, then reads "
                     "the whole train. In the last 3 boxes he writes the word by himself.", "engine")
        rh = (y - 36) / len(words)
        for i, word in enumerate(words):
            top = y - i * rh
            base = top - rh + 22
            pic(c, word, 44, top - rh / 2, rh - 16, theme)
            train(c, 96, base, word, theme)
            for k in range(3):
                tile(c, 420 + k * 40, base + 10, 36, 40, "", theme, blank=True)
        k_footer(c, W)
    return draw


def garage(day, theme, families, tag):
    KEY.append((f"Day {day} · Park the Cars", [w for _, ws in families for w in ws]))

    def draw(c, W, H):
        y = k_header(c, W, H, theme, tag, "Park the Cars: Word Families",
                     "Words in a family end the same way. Rudhra drives a car (or his finger) to each spot, "
                     "writes the car's letter in the empty box, and reads the word.", "car")
        sec_h = (y - 36) / len(families)
        for f, (end, words) in enumerate(families):
            top = y - f * sec_h
            card(c, 0, top - 44, 150, 40, theme, fill=True)
            text(c, 75, top - 34, f"-{end} garage", 18, B, theme[1], "c")
            for k, w in enumerate(words):
                cx = 190 + k * 86
                ICONS["car"](c, cx, top - 22, 46)
                c.setFillColor(WHITE)
                c.circle(cx - 2, top - 15, 9, stroke=0, fill=1)
                text(c, cx - 2, top - 20, w[0], 14, B, INK, "c")
            cw = W / len(words)
            ch = sec_h - 58
            for k, w in enumerate(words):
                x = k * cw
                card(c, x + 4, top - 52 - ch, cw - 8, ch, theme)
                pic(c, w, x + cw / 2, top - 52 - ch * 0.38, min(ch * 0.62, cw - 30))
                tw = min(38, (cw - 30) / 3)
                for j, ch_ in enumerate(w):
                    tile(c, x + cw / 2 - 1.5 * tw - 3 + j * (tw + 3), top - 52 - ch + 10, tw, tw * 1.1,
                         "" if j == 0 else ch_, theme, blank=(j == 0))
        k_footer(c, W)
    return draw


def connect_wires(day, theme, words, tag):
    rng = random.Random(100 + day)
    right = words[:]
    rng.shuffle(right)
    KEY.append((f"Day {day} · Wire It Up", [f"{w} → picture of a {w}" for w in words]))

    def draw(c, W, H):
        y = k_header(c, W, H, theme, tag, "Wire It Up!",
                     "Rudhra reads each word, then draws a wire from its plug to the matching picture's plug. "
                     "Use a different crayon color for each wire, like real wires!", "toolbox")
        rh = (y - 36) / len(words)
        for i, w in enumerate(words):
            cy = y - i * rh - rh / 2
            card(c, 10, cy - 30, 150, 60, theme)
            text(c, 85, cy - 13, w, 38, R, INK, "c")
            plug(c, 172, cy, WIRE[i % len(WIRE)])
            plug(c, 400, cy, GRAY)
            pic(c, right[i], 470, cy, min(rh - 10, 88), theme)
        k_footer(c, W)
    return draw


def fix_it(day, theme, items, tag):
    KEY.append((f"Day {day} · Fix-It Shop", [f"{w} (missing {w[1]})" for w, _ in items]))

    def draw(c, W, H):
        y = k_header(c, W, H, theme, tag, "Fix-It Shop: Broken Words",
                     "Each word lost its middle sound! Rudhra says the picture slowly (\"c...a...t\"), circles the "
                     "letter from the toolbox that fixes it, and writes it in the empty box.", "wrench")
        cw, ch = W / 2, (y - 36) / 3
        for i, (w, opts) in enumerate(items):
            r, k = divmod(i, 2)
            x, top = k * cw, y - r * ch
            card(c, x + 4, top - ch + 6, cw - 8, ch - 10, theme)
            pic(c, w, x + 64, top - ch / 2, min(ch - 40, 100))
            for j, letter in enumerate(w):
                tile(c, x + 128 + j * 42, top - ch / 2 + 2, 38, 44, "" if j == 1 else letter, theme, 30, blank=(j == 1))
            ICONS["toolbox"](c, x + 140, top - ch + 40, 38)
            for j, o in enumerate(opts):
                c.setStrokeColor(theme[1])
                c.setLineWidth(1.2)
                c.setFillColor(WHITE)
                c.circle(x + 180 + j * 30, top - ch + 40, 13, stroke=1, fill=1)
                text(c, x + 180 + j * 30, top - ch + 34, o, 17, R, TH["t"][1], "c")
        k_footer(c, W)
    return draw


def bus_stop(day, theme, words, tag):
    KEY.append((f"Day {day} · Which Bus Stop?", [f"{w}: {w[1]}" for w in words]))

    def draw(c, W, H):
        y = k_header(c, W, H, theme, tag, "Which Bus Stop? Middle Sounds",
                     "Rudhra says the picture slowly and listens for the MIDDLE sound. He circles that bus stop. "
                     "(Tip: stretch the word — \"b...uuu...s\".)", "bus")
        cw, ch = W / 2, (y - 36) / 4
        for i, w in enumerate(words):
            r, k = divmod(i, 2)
            x, top = k * cw, y - r * ch
            card(c, x + 4, top - ch + 6, cw - 8, ch - 10, theme)
            pic(c, w, x + 56, top - ch / 2, min(ch - 26, 84))
            for j, v in enumerate(VOWELS):
                sx = x + 118 + j * 30
                c.setStrokeColor(GRAY)
                c.setLineWidth(2)
                c.line(sx, top - ch / 2 - 26, sx, top - ch / 2 - 6)
                c.setStrokeColor(theme[1])
                c.setFillColor(WHITE)
                c.setLineWidth(1.4)
                c.circle(sx, top - ch / 2 + 6, 13, stroke=1, fill=1)
                text(c, sx, top - ch / 2, v, 17, R, TH["t"][1], "c")
        k_footer(c, W)
    return draw


def word_builder(day, theme, words, tag):
    KEY.append((f"Day {day} · Build the Word", words))
    bank = sorted(set("".join(words)))

    def draw(c, W, H):
        y = k_header(c, W, H, theme, tag, "Build the Word (Spelling)",
                     "Rudhra says the picture, taps one finger per sound, and writes one letter in each box. "
                     "He can copy letters from the letter bank. Cut-out letter tiles work great here too!", "toolbox")
        n = len(bank)
        tw = min(34, (W - 10) / n - 3)
        for j, ch in enumerate(bank):
            tile(c, j * (tw + 3), y - 38, tw, 34, ch, theme, 22, fill=theme[0])
        y -= 50
        cw, ch = W / 2, (y - 36) / 4
        for i, w in enumerate(words):
            r, k = divmod(i, 2)
            x, top = k * cw, y - r * ch
            card(c, x + 4, top - ch + 6, cw - 8, ch - 10, theme)
            pic(c, w, x + 56, top - ch / 2, min(ch - 24, 86))
            for j in range(3):
                tile(c, x + 116 + j * 46, top - ch / 2 - 22, 40, 46, "", theme, blank=True)
        k_footer(c, W)
    return draw


def read_match(day, theme, rows, tag):
    KEY.append((f"Day {day} · Read & Circle", [f"{p} → {a}" for p, _, a in rows]))

    def draw(c, W, H):
        y = k_header(c, W, H, theme, tag, "Read & Circle",
                     "Rudhra reads the words (help with the little word \"a\"). He circles the picture that "
                     "matches. Careful — the pictures rhyme!", "sun")
        rh = (y - 36) / len(rows)
        for i, (phrase, opts, _) in enumerate(rows):
            cy = y - i * rh - rh / 2
            text(c, 0, cy - 10, phrase, 28, R)
            for k, name in enumerate(opts):
                pic(c, name, 270 + k * 96, cy, min(rh - 12, 84), theme)
        k_footer(c, W)
    return draw


def read_draw(day, theme, phrases, tag):
    KEY.append((f"Day {day} · Read & Draw", ["Any drawing that shows the words is right!"]))

    def draw(c, W, H):
        y = k_header(c, W, H, theme, tag, "Read & Draw",
                     "Rudhra reads each box and draws it. Ask him to point to the part of his picture that "
                     "shows each word.", "pen")
        cw, ch = W / 2, (y - 36) / 2
        for i, ph in enumerate(phrases):
            r, k = divmod(i, 2)
            x, top = k * cw, y - r * ch
            card(c, x + 4, top - ch + 6, cw - 8, ch - 10, theme)
            text(c, x + cw / 2, top - 40, ph, 26, R, INK, "c")
        k_footer(c, W)
    return draw


def scene(c, parts, x, y, s):
    for name, dx, dy, k in parts:
        ICONS[name](c, x + dx * s, y + dy * s, s * k)


def silly(day, theme, items, tag):
    KEY.append((f"Day {day} · Silly or Not?", [f"{t} → {'YES' if a else 'NO'}" for t, _, a in items]))

    def draw(c, W, H):
        y = k_header(c, W, H, theme, tag, "Yes or No? Look & Read",
                     "Teach the \"heart words\" first: the, is, in, on, has. Rudhra reads the sentence, looks at the "
                     "picture, and circles YES if it matches or NO if it doesn't.", "sun")
        cw, ch = W / 2, (y - 36) / 3
        for i, (sent, parts, _) in enumerate(items):
            r, k = divmod(i, 2)
            x, top = k * cw, y - r * ch
            card(c, x + 4, top - ch + 6, cw - 8, ch - 10, theme)
            scene(c, parts, x + cw / 2, top - ch * 0.52, ch * 0.42)
            text(c, x + cw / 2, top - 26, sent, 15.5, R, INK, "c")
            for j, (lab, col) in enumerate((("YES", TH[2][1]), ("NO", TH["t"][1]))):
                bx = x + 30 + j * (cw - 112)
                c.setStrokeColor(col)
                c.setLineWidth(1.4)
                c.roundRect(bx, top - ch + 16, 46, 24, 8, stroke=1, fill=0)
                text(c, bx + 23, top - ch + 23, lab, 12, B, col, "c")
        k_footer(c, W)
    return draw


def reading_check(day, theme, words, tag):
    KEY.append((f"Day {day} · Reading Check", ["Tick each word he reads; 15+ is a big win!"]))

    def draw(c, W, H):
        y = k_header(c, W, H, theme, tag, "Show What You Can Read!",
                     "No pictures, no rush. Rudhra reads each word; tick the box when he does. Let him sound it "
                     "out — that counts! Celebrate, then give him the certificate.", "solar")
        cols, rows = 4, math.ceil(len(words) / 4)
        cw, ch = W / cols, (y - 90) / rows
        for i, w in enumerate(words):
            r, k = divmod(i, cols)
            x, top = k * cw, y - r * ch
            card(c, x + 5, top - ch + 6, cw - 10, ch - 10, theme)
            text(c, x + cw / 2, top - ch / 2 - 10, w, 34, R, INK, "c")
            c.setStrokeColor(GRAY)
            c.rect(x + cw - 30, top - 30, 14, 14, stroke=1, fill=0)
        text(c, W / 2, 50, f"{NAME} read ______ words!", 22, B, theme[1], "c")
        k_footer(c, W)
    return draw


# ---------------------------------------------------------------- extras
def word_cards(words, page_no, total):
    def draw(c, W, H):
        text(c, 0, H - 20, f"Picture Word Cards ({page_no} of {total})", 18, B, TH["x"][1])
        para(c, 0, H - 36, "✂ Cut out. Use for the Word Train, Solar Power, Bus Stop and Wire It Up games. "
             "Fold the picture back to test reading without it!", W, 10)
        cols, rows = 3, 4
        cw, ch = W / cols, (H - 50) / rows
        for i, w in enumerate(words):
            r, k = divmod(i, cols)
            x, top = k * cw, H - 48 - r * ch
            c.setStrokeColor(GRAY)
            c.setLineWidth(0.8)
            c.rect(x, top - ch, cw, ch, stroke=1, fill=0)
            c.setDash(3, 3)
            c.line(x + 8, top - ch * 0.62, x + cw - 8, top - ch * 0.62)
            c.setDash()
            ICONS[w](c, x + cw / 2, top - ch * 0.31, ch * 0.5)
            text(c, x + cw / 2, top - ch * 0.88, w, 38, R, INK, "c")
    return draw


def letter_tiles(letters, title):
    def draw(c, W, H):
        text(c, 0, H - 20, title, 18, B, TH["x"][1])
        text(c, 0, H - 38, "✂ Cut out the tiles. Tape them on toy train cars or blocks. Vowels are red.", 10)
        cols = 6
        rows = math.ceil(len(letters) / cols)
        cw, ch = W / cols, min(110, (H - 50) / rows)
        for i, l in enumerate(letters):
            r, k = divmod(i, cols)
            x, top = k * cw, H - 48 - r * ch
            c.setStrokeColor(GRAY)
            c.setLineWidth(0.8)
            c.rect(x, top - ch, cw, ch, stroke=1, fill=0)
            text(c, x + cw / 2, top - ch / 2 - 20, l, 60, R, TH["t"][1] if l in VOWELS else INK, "c")
    return draw


def bingo():
    rng = random.Random(77)
    pool_ = ["cat", "hat", "van", "map", "bag", "dog", "box", "pot", "mop", "pig", "pin", "lid",
             "bus", "sun", "cup", "bug", "bed", "hen", "net", "jet"]

    def draw(c, W, H):
        text(c, 0, H - 22, "Robot Bingo", 22, B, TH["x"][1])
        para(c, 0, H - 40, "Grown-up calls a robot word (\"b-u-s\"). Players blend it and cover the picture with a "
             "coin. 3 in a row wins! Later, call the word by showing a word card instead.", W, 10.5)
        size = 68
        for b in range(4):
            x0 = (b % 2) * W / 2 + (W / 2 - 3 * size) / 2
            top = H - 82 - (b // 2) * (3 * size + 34)
            text(c, x0 + 1.5 * size, top + 4, f"Board {b + 1}", 13, B, TH["x"][1], "c")
            for i, w in enumerate(rng.sample(pool_, 9)):
                r, k = divmod(i, 3)
                c.setStrokeColor(TH["x"][1])
                c.setLineWidth(1)
                c.setFillColor(WHITE)
                c.rect(x0 + k * size, top - 8 - (r + 1) * size, size, size, stroke=1, fill=1)
                ICONS[w](c, x0 + k * size + size / 2, top - 8 - r * size - size / 2, size * 0.78)
        y = H - 82 - 2 * (3 * size + 34) - 10
        text(c, 0, y, "Calling list (tick as you call)", 13, B, TH["x"][1])
        for i, w in enumerate(pool_):
            r, k = divmod(i, 5)
            text(c, k * W / 5, y - 26 - r * 24, f"☐  {'-'.join(w)}", 14)
    return draw


def solar_chart(c, W, H):
    T = TH["x"]
    text(c, W / 2, H - 30, f"{NAME}'s Solar Power Chart", 26, B, T[1], "c")
    text(c, W / 2, H - 52, "Color one solar cell after each day. Fill them all to charge the battery!", 12, R, INK, "c")
    ICONS["sun"](c, 80, H - 110, 90)
    cols, rows, cell = 5, 4, 82
    x0, top = (W - cols * cell) / 2 + 20, H - 140
    c.setFillColor(colors.HexColor("#1F4E8C"))
    c.roundRect(x0 - 10, top - rows * cell - 10, cols * cell + 20, rows * cell + 20, 8, stroke=0, fill=1)
    for i in range(cols * rows):
        r, k = divmod(i, cols)
        c.setFillColor(WHITE)
        c.setStrokeColor(ICON_LBLU)
        c.setLineWidth(2)
        c.rect(x0 + k * cell + 3, top - (r + 1) * cell + 3, cell - 6, cell - 6, stroke=1, fill=1)
        text(c, x0 + k * cell + 12, top - r * cell - 18, i + 1, 11, B, GRAY)
    yb = top - rows * cell - 50
    wire(c, [(W / 2, top - rows * cell - 10), (W / 2 - 120, yb - 40)], WIRE[0], 5)
    wire(c, [(W / 2 + 20, top - rows * cell - 10), (W / 2 + 120, yb - 40)], WIRE[1], 5)
    bx, by = W / 2 - 170, yb - 120
    c.setStrokeColor(INK)
    c.setLineWidth(2)
    c.setFillColor(WHITE)
    c.roundRect(bx, by, 100, 70, 8, stroke=1, fill=1)
    c.rect(bx + 100, by + 25, 10, 20, stroke=1, fill=1)
    for k in range(4):
        c.rect(bx + 8 + k * 23, by + 8, 18, 54, stroke=1, fill=0)
    text(c, bx + 50, by - 18, "Battery", 12, B, INK, "c")
    ICONS["bulb"](c, W / 2 + 140, yb - 80, 90)
    text(c, W / 2 + 140, by - 18, "Light!", 12, B, INK, "c")
    text(c, W / 2, 22, "Color a battery bar every 5 days. When all are full → certificate time!", 12, R, INK, "c")


def vowel_poster(c, W, H):
    text(c, W / 2, H - 30, "The 5 Vowel Sounds", 28, B, TH["t"][1], "c")
    text(c, W / 2, H - 54, "Every 3-letter word has one of these in the middle. Say the short sound!", 12, R, INK, "c")
    vs = [("a", "apple", TH[3]), ("e", "egg", TH[2]), ("i", "igloo", TH[1]), ("o", "octopus", TH[4]),
          ("u", "umbrella", TH["x"])]
    rh = 104
    for i, (v, w, th) in enumerate(vs):
        top = H - 70 - i * rh
        card(c, 0, top - rh + 6, W, rh - 8, th, fill=True, radius=14)
        text(c, 60, top - rh / 2 - 26, v, 72, R, TH["t"][1], "c")
        ICONS[w](c, 190, top - rh / 2 + 2, 82)
        text(c, 260, top - rh / 2 + 4, w, 28, R, INK)
        text(c, 260, top - rh / 2 - 22, f"/{v}/ as in {w}", 13, R, th[1])
    y = H - 70 - 5 * rh - 16
    card(c, 0, y - 112, W, 112, TH["x"], radius=14)
    text(c, W / 2, y - 24, "How to read a word:  Sound it → Slide it → Say it!", 16, B, TH["x"][1], "c")
    for k, ch in enumerate("bus"):
        tile(c, 120 + k * 62, y - 92, 52, 52, ch, TH["x"])
    pts = [(146 + k * 62, y - 100) for k in range(3)] + [(340, y - 100)]
    wire(c, pts, WIRE[0])
    for x, yy in pts[:3]:
        plug(c, x, yy, WIRE[0])
    ICONS["bulb"](c, 350, y - 68, 56)
    ICONS["bus"](c, 450, y - 68, 70)


def certificate(c, W, H):
    T = TH[1]
    c.setStrokeColor(T[1])
    c.setLineWidth(6)
    c.roundRect(10, 60, W - 20, H - 120, 20, stroke=1, fill=0)
    c.setLineWidth(1.5)
    c.setStrokeColor(TH[3][1])
    c.roundRect(24, 74, W - 48, H - 148, 14, stroke=1, fill=0)
    for k, name in enumerate(("engine", "bus", "solar", "car")):
        ICONS[name](c, 110 + k * 110, H - 150, 80)
    text(c, W / 2, H - 240, "Certificate of", 24, R, INK, "c")
    text(c, W / 2, H - 290, "Super Word Engineer", 38, B, T[1], "c")
    text(c, W / 2, H - 350, "proudly awarded to", 15, R, INK, "c")
    text(c, W / 2, H - 410, NAME, 48, B, TH[3][1], "c")
    text(c, W / 2, H - 460, "for powering up 3-letter words: sounding, sliding and saying them!", 13, R, INK, "c")
    write_line(c, 70, H - 560, 250)
    write_line(c, W - 250, H - 560, W - 70)
    text(c, 160, H - 578, "Date", 11, R, GRAY, "c")
    text(c, W - 160, H - 578, "Signed", 11, R, GRAY, "c")
    for k in range(5):
        star(c, W / 2 - 100 + k * 50, 120, 14, ICON_YEL)


def cover(c, W, H):
    c.setFillColor(TH[1][0])
    c.roundRect(0, H - 200, W, 200, 18, stroke=0, fill=1)
    text(c, W / 2, H - 70, f"{NAME}'s", 34, B, TH[3][1], "c")
    text(c, W / 2, H - 120, "Word Workshop", 44, B, TH[1][1], "c")
    text(c, W / 2, H - 160, "Reading 3-letter words · Kindergarten", 15, R, INK, "c")
    ICONS["sun"](c, W - 70, H - 240, 80)
    ICONS["solar"](c, 70, H - 250, 90)
    train(c, 70, H - 400, "cat", TH[1], trace=False, car_w=80)
    for k, w in enumerate(("bus", "dog", "pig", "sun", "hen")):
        ICONS[w](c, 70 + k * 100, H - 460, 76)
    text(c, W / 2, 205, "Sound it  →  Slide it  →  Say it!", 20, B, TH[3][1], "c")
    ICONS["car"](c, 120, 160, 100)
    ICONS["bus"](c, W - 120, 160, 120)
    for k, (wk, nm) in enumerate([("Week 1", "short a"), ("Week 2", "short o, i"), ("Week 3", "short u, e"),
                                  ("Week 4", "Read it!")]):
        th = [TH[1], TH[2], TH[3], TH[4]][k]
        card(c, k * W / 4 + 4, 60, W / 4 - 8, 50, th, fill=True)
        text(c, k * W / 4 + W / 8, 90, wk, 12, B, th[1], "c")
        text(c, k * W / 4 + W / 8, 72, nm, 10, R, INK, "c")


# ---------------------------------------------------------------- parent guide
PLAN = [
    (1, "Short a", [(1, "Robot Ears", "hear the sounds in a word and blend them"),
                    (2, "Power the Bulb (a)", "read a-words: cat, hat, van, map, bag, fan"),
                    (3, "Load the Train (a)", "trace and write a-words"),
                    (4, "Park the Cars: -at, -an", "word families: change the first sound"),
                    (5, "Wire It Up (a)", "read a word and match its picture")]),
    (2, "Short o and i", [(6, "Robot Ears (o, i)", "hear o and i in the middle"),
                          (7, "Power the Bulb (o)", "read dog, log, box, pot, mop, top"),
                          (8, "Load the Train (i)", "trace and write pig, lid, pin, bin, six"),
                          (9, "Park the Cars: -ot, -ig, -in", "more word families"),
                          (10, "Fix-It Shop (a, o, i)", "find the missing middle sound")]),
    (3, "Short u and e", [(11, "Robot Ears (u, e)", "hear u and e in the middle"),
                          (12, "Power the Bulb (u)", "read bus, sun, cup, bug, nut, rug"),
                          (13, "Load the Train (e)", "trace and write bed, hen, net, pen, jet"),
                          (14, "Fix-It Shop (all)", "choose between vowels"),
                          (15, "Wire It Up (u, e)", "read and match")]),
    (4, "Read it!", [(16, "Which Bus Stop?", "pick the middle sound of any word"),
                     (17, "Build the Word", "spell a word: one letter per sound"),
                     (18, "Read & Circle", "read short phrases (\"a big pig\")"),
                     (19, "Read & Draw", "read and show understanding"),
                     (20, "Yes or No? + Reading Check", "read sentences; celebrate!")]),
]

DAYS = {
    1: ("Play Robot Talk for 3 minutes: say \"c-a-t\" like a robot; he says \"cat!\". Then do the page.",
        "Use only your voice, no letters yet. If he struggles, use 2 sounds: \"c-at\"."),
    2: ("Build \"cat\" with letter tiles on 3 toy train cars. Touch each car: /k/ /a/ /t/. Push the train "
        "fast and say \"cat!\". Then the page.", "Say SOUNDS, not letter names: c says /k/, not \"see\"."),
    3: ("Show how to trace: start at the top, say the sound while tracing.", "Big, wobbly letters are fine. "
        "Saying the sound while writing is what matters."),
    4: ("Make \"cat\" with tiles. Swap the c for h: \"hat\"! Swap for r: \"rat\". He's changing just one part, "
        "like swapping a wheel.", "Point out the rhyme: cat, hat, rat, bat all sound the same at the end."),
    5: ("Lay 3 picture cards and 3 word cards on the floor; he connects them with string or pipe cleaners. "
        "Then the page.", "Let him check by blending, not by guessing from the first letter."),
    6: ("Robot Talk with o and i words: d-o-g, p-i-g, b-o-x. Show the vowel poster: o octopus, i igloo.",
        "o and i can sound alike to young ears — exaggerate the mouth: o is a round mouth, i is a smile."),
    7: ("Tile train again: d-o-g. Then change d to l: log!", "If he says \"dog\" for \"log\", ask: what's the "
        "FIRST sound? Point to it."),
    8: ("Trace and say: /p/ /i/ /g/.", "Keep i short: \"ih\", like itchy."),
    9: ("Tile families: pot → dot → hot. pig → wig → dig.", "Make it a race: how many words can he make by "
        "changing only the first tile?"),
    10: ("Fix-It Shop game first: show c_t with tiles; he tries a, o, i in the gap and reads each one. Which is "
         "a real word that matches the picture?", "\"cot\" and \"cit\" are funny — laughing helps him notice "
         "the middle sound."),
    11: ("Robot Talk with u and e words: b-u-s, b-e-d. Show the vowel poster: u umbrella, e egg.",
         "e and i are the hardest pair. Exaggerate: e is \"eh\" (egg), i is \"ih\" (itch)."),
    12: ("Tile train: s-u-n. Then he picks a card from the pile and reads it to \"charge\" the solar panel.",
         "u is \"uh\" like umbrella."),
    13: ("Trace and say: /b/ /e/ /d/.", "Bed: draw a little bed on the b and d if he mixes them up."),
    14: ("Fix-It Shop with tiles, all vowels.", "If stuck, say the word slowly and stretch the middle: "
         "\"s...uuu...n\"."),
    15: ("Wire It Up with string on the floor first, then the page.", "Mix in a few word cards from earlier weeks."),
    16: ("Bus Stop game: 5 vowel cards on the floor as bus stops; he drives his school bus to the right stop for "
         "each picture card.", "Stretch the word and freeze on the middle: \"h...eeeee...n\"."),
    17: ("Tap one finger per sound before writing: /s/ /u/ /n/ — 3 fingers, 3 boxes.", "Spelling is harder than "
         "reading. Let him use the tiles or the letter bank."),
    18: ("Teach the word \"a\" as a heart word (just know it by heart).", "If he guesses from the picture, cover "
         "the pictures until he has read the words."),
    19: ("He reads each box, then draws. Ask: \"Show me the red part!\"", "Drawing shows he understood — that's "
         "real reading."),
    20: ("Teach heart words: the, is, in, on, has (read them together 3 times). Do Yes or No, then the Reading "
         "Check. Give the certificate!", "Count any word he sounds out and gets right. Celebrate big!"),
}

GAMES = [
    ("Robot Talk", "nothing",
     "You talk like a robot: \"Get your c-u-p!\" He blends and does it. Then he's the robot and you guess."),
    ("Word Train", "letter tiles + toy train",
     "Tape tiles on 3 train cars. He touches each car saying its sound, then pushes the train fast and says the "
     "word. Swap the first car to make a new word."),
    ("Solar Power Reading", "word cards + his solar panel toy or a sunny window",
     "Each word he reads \"charges\" the panel. 5 words = color a cell on the Solar Power Chart."),
    ("Bus Stop", "vowel cards + toy school bus",
     "Put a, e, i, o, u cards on the floor as bus stops. Show a picture card; he drives the bus to the stop "
     "for its middle sound."),
    ("Park the Cars", "toy cars + paper garages",
     "Label garages -at, -og, -ug. Put a letter on each car. He parks a car and reads the word it makes."),
    ("Fix-It Shop", "tiles + his toy tools",
     "Make a \"broken\" word (c-o-t under a cat picture). He uses a toy wrench to swap the broken tile."),
    ("Wire It Up", "string, yarn or pipe cleaners",
     "Word cards on one side, picture cards on the other. He connects each pair with a \"wire\"."),
    ("Mouse Click Words", "computer + mouse",
     "Open a blank document with a huge font (150+). He types a word he just read, then clicks to change its "
     "color. Typing one finger at a time is great sound-by-sound practice."),
    ("Robot Bingo", "Bingo page + coins", "Call robot words; he covers the pictures. 3 in a row wins."),
]

SOUNDS = [("a", "apple"), ("b", "bus"), ("c", "cat (says /k/)"), ("d", "dog"), ("e", "egg"), ("f", "fan"),
          ("g", "gum (hard g)"), ("h", "hat"), ("i", "igloo"), ("j", "jet"), ("k", "kite"), ("l", "log"),
          ("m", "map"), ("n", "net"), ("o", "octopus"), ("p", "pig"), ("q", "queen (qu)"), ("r", "rat"),
          ("s", "sun"), ("t", "top"), ("u", "umbrella"), ("v", "van"), ("w", "web"), ("x", "box (ends /ks/)"),
          ("y", "yo-yo"), ("z", "zip")]


def guide_story():
    s = [P(f"How to Teach {NAME} 3-Letter Words", "h1")]
    s.append(P(f"Reading words like <b>cat, bus</b> and <b>sun</b> is the big first step in reading. {NAME} learns "
               "three things: <b>hearing</b> the sounds in a word, <b>matching</b> letters to sounds, and "
               "<b>blending</b> sounds into a word. This book turns each word into something he loves: a circuit to "
               "power up, a train to load, a car to park, or a broken thing to fix."))
    s.append(P("The big idea: Sound it → Slide it → Say it", "h2"))
    s += bullets(["<b>Sound it:</b> touch each letter and say its sound: /k/ /a/ /t/.",
                  "<b>Slide it:</b> slide a finger (or a toy car!) under the letters, joining the sounds: "
                  "\"caaaat\". This is the electricity running along the wire.",
                  "<b>Say it:</b> say it fast like a real word: \"cat!\" The bulb lights up!"])
    s.append(P("Say the sounds the right way", "h2"))
    s += bullets([
        "Use <b>sounds, not letter names</b>: \"c\" says /k/, not \"see\".",
        "Keep sounds short and clean, with no extra \"uh\": say \"mmm\", not \"muh\"; \"sss\", not \"suh\".",
        "Short vowels: <b>a</b> as in apple, <b>e</b> as in egg, <b>i</b> as in igloo, <b>o</b> as in octopus, "
        "<b>u</b> as in umbrella. See the Vowel Sounds poster."])
    s.append(P("Each day: 10–15 minutes (he's 5!)", "h2"))
    rows = [["Step", "Time", "What to do"],
            ["1. Robot Talk", "2 min", "Say robot words (\"b-u-s\"); he blends them. No paper needed."],
            ["2. Build it", "3–5 min", "Make today's words with letter tiles on his toy train cars or blocks."],
            ["3. Page", "5 min", "One activity page. Read the Grown-up line at the top first."],
            ["4. Play", "3–5 min", "One game from the Games page, then color a star and a solar cell."]]
    s.append(table(rows, [90, 60, FW - 150], TH[1]))
    s.append(P("Tips for a tinkerer", "h2"))
    s += bullets([
        "Let him be the <b>engineer</b>: he powers bulbs, connects wires and fixes broken words. Call it his work, "
        "not homework.",
        "Let him <b>hold a toy car</b> and drive it under the letters while blending. Moving hands help busy kids focus.",
        "<b>Stop while he's still having fun.</b> Two short sessions beat one long one.",
        "<b>Go at his pace.</b> If a week feels hard, repeat it. Many kids need several weeks per vowel, and that's normal.",
        "Praise the work: \"You said every sound, then slid them together. That's how readers do it!\""])
    s.append(PageBreak())

    s.append(P("Before You Start: Sound Check", "h1"))
    s.append(P("Point to each letter and ask, \"What sound does it make?\" Tick the ones he knows. If he misses some, "
               "teach 2–3 new sounds a day with the letter tiles while you go. Weeks 1–2 only need: "
               "<b>a, b, c, d, f, g, h, i, l, m, n, o, p, r, s, t, v, w, x</b>."))
    rows = [["Letter", "Sound as in", "Knows it?"] * 2]
    half = (len(SOUNDS) + 1) // 2
    for i in range(half):
        row = []
        for j in (i, i + half):
            if j < len(SOUNDS):
                l, w = SOUNDS[j]
                row += [l, w, "☐"]
            else:
                row += ["", "", ""]
        rows.append(row)
    tb = Table(rows, colWidths=[50, 140, 70] * 2)
    tb.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.6, TH[2][1]), ("BACKGROUND", (0, 0), (-1, 0), TH[2][0]),
                            ("FONTNAME", (0, 0), (-1, -1), R), ("FONTNAME", (0, 0), (-1, 0), B),
                            ("FONTNAME", (0, 1), (0, -1), B), ("FONTNAME", (3, 1), (3, -1), B),
                            ("FONTSIZE", (0, 0), (-1, -1), 11), ("ALIGN", (2, 0), (2, -1), "CENTER"),
                            ("ALIGN", (5, 0), (5, -1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                            ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    s += [tb, PageBreak()]
    s.append(P("4-Week Plan at a Glance", "h1"))
    for wk, name, days in PLAN:
        th = TH[wk]
        rows = [[f"Week {wk}: {name}", "", ""]] + [[str(d), t, g] for d, t, g in days]
        tb = Table([[Paragraph(esc(x), ST["cellb" if r == 0 or i == 1 else "cell"]) for i, x in enumerate(row)]
                    for r, row in enumerate(rows)], colWidths=[34, 190, FW - 224])
        tb.setStyle(TableStyle([("SPAN", (0, 0), (-1, 0)), ("BACKGROUND", (0, 0), (-1, 0), th[0]),
                                ("GRID", (0, 0), (-1, -1), 0.6, th[1]), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                                ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
        s += [tb, Spacer(1, 6)]
    s.append(PageBreak())

    s.append(P("What to Do Each Day", "h1"))
    titles = {d: t for _, _, days in PLAN for d, t, _ in days}
    for wk, name, days in PLAN:
        s.append(P(f"Week {wk}: {esc(name)}", "h2"))
        for d, _, _ in days:
            do, tipx = DAYS[d]
            col = TH[wk][1].hexval().replace("0x", "#")
            s.append(KeepTogether([
                P(f"<font color='{col}'><b>Day {d} · {esc(titles[d])}</b></font>", "body"),
                P(f"<b>Do:</b> {esc(do)}", "note"), P(f"<b>Tip:</b> {esc(tipx)}", "note"), Spacer(1, 3)]))
    s.append(PageBreak())

    s.append(P(f"Games {NAME} Will Love", "h1"))
    s.append(P("Play one game every day, and use games instead of pages whenever he is tired. Games ARE learning."))
    s.append(table([["Game", "You need", "How to play"]] + [list(g) for g in GAMES], [105, 120, FW - 225], TH[3]))
    s.append(P("When to move on", "h2"))
    s += bullets(["He can read most of the week's words by sounding them out (it's fine if he's still slow).",
                  "If not, repeat the week: replay the games, rebuild words with tiles, and reprint the pages.",
                  "After the 4 weeks: keep 5 minutes a day of word cards and Robot Talk. Next step: 4-letter words "
                  "like \"stop\" and \"frog\"."])
    s.append(PageBreak())
    return s


def build():
    T1, T2, T3, T4 = TH[1], TH[2], TH[3], TH[4]
    w1 = [
        listen_circle(1, T1, [("cat", ["cat", "dog", "sun"]), ("hat", ["bus", "hat", "pig"]),
                              ("van", ["van", "bed", "cup"]), ("map", ["log", "web", "map"]),
                              ("bag", ["bag", "pin", "hen"])], "Week 1 · Day 1"),
        power_bulb(2, T1, [("cat", "dog"), ("hat", "cap"), ("van", "bus"), ("map", "mop"), ("bag", "bug"),
                           ("fan", "pan")], "Week 1 · Day 2"),
        word_train(3, T1, ["can", "pan", "rat", "bat", "cap"], "Week 1 · Day 3"),
        garage(4, T1, [("at", ["cat", "hat", "rat", "bat"]), ("an", ["van", "can", "fan", "pan"])], "Week 1 · Day 4"),
        connect_wires(5, T1, ["cat", "van", "map", "bag", "fan", "hat"], "Week 1 · Day 5"),
    ]
    w2 = [
        listen_circle(6, T2, [("dog", ["dog", "cat", "bus"]), ("pig", ["hen", "pig", "van"]),
                              ("box", ["box", "sun", "hat"]), ("pin", ["jet", "map", "pin"]),
                              ("mop", ["mop", "bed", "fan"])], "Week 2 · Day 6"),
        power_bulb(7, T2, [("dog", "cat"), ("box", "bus"), ("pot", "pan"), ("mop", "map"), ("log", "leg"),
                           ("top", "hat")], "Week 2 · Day 7"),
        word_train(8, T2, ["pig", "lid", "pin", "bin", "six"], "Week 2 · Day 8"),
        garage(9, T2, [("ot", ["pot", "dot", "hot"]), ("ig", ["pig", "wig", "dig"]), ("in", ["pin", "bin", "fin"])],
               "Week 2 · Day 9"),
        fix_it(10, T2, [("cat", "aoi"), ("dog", "aoi"), ("pig", "aoi"), ("box", "aoi"), ("six", "aoi"),
                        ("van", "aoi")], "Week 2 · Day 10"),
    ]
    w3 = [
        listen_circle(11, T3, [("bus", ["bus", "box", "pig"]), ("bed", ["cat", "bed", "mop"]),
                               ("sun", ["hen", "dog", "sun"]), ("net", ["net", "bag", "cup"]),
                               ("bug", ["pan", "bug", "lid"])], "Week 3 · Day 11"),
        power_bulb(12, T3, [("bus", "van"), ("sun", "six"), ("cup", "cap"), ("bug", "rug"), ("nut", "net"),
                            ("rug", "bag")], "Week 3 · Day 12"),
        word_train(13, T3, ["bed", "hen", "net", "pen", "jet"], "Week 3 · Day 13"),
        fix_it(14, T3, [("bus", "aeu"), ("bed", "aeu"), ("sun", "aeu"), ("hen", "aeu"), ("cup", "aeu"),
                        ("web", "aeu")], "Week 3 · Day 14"),
        connect_wires(15, T3, ["tub", "hut", "net", "leg", "web", "ten"], "Week 3 · Day 15"),
    ]
    w4 = [
        bus_stop(16, T4, ["cat", "hen", "pig", "dog", "bus", "jet", "fin", "mop"], "Week 4 · Day 16"),
        word_builder(17, T4, ["sun", "pig", "bed", "cat", "dog", "cup", "hen", "box"], "Week 4 · Day 17"),
        read_match(18, T4, [("a big pig", ["wig", "pig", "dig"], "pig"), ("a red hat", ["hat", "cat", "bat"], "hat"),
                            ("a hot pot", ["dot", "top", "pot"], "pot"), ("a fat rat", ["cat", "rat", "bat"], "rat"),
                            ("a wet net", ["jet", "net", "web"], "net"), ("a big bug", ["bus", "rug", "bug"], "bug")],
                   "Week 4 · Day 18"),
        read_draw(19, T4, ["a red sun", "a big bus", "a cat in a box", "ten red dots"], "Week 4 · Day 19"),
        silly(20, T4, [("The cat is in the box.", [("box", 0, -0.12, 0.85), ("cat", 0, 0.38, 0.55)], True),
                       ("The bug is on the rug.", [("rug", 0, -0.05, 1.0), ("bug", 0.05, 0.05, 0.42)], True),
                       ("The dog is on the bed.", [("log", 0, -0.25, 1.0), ("dog", 0, 0.32, 0.6)], False),
                       ("The pig has a hat.", [("pig", 0, -0.08, 0.85), ("hat", 0, 0.45, 0.5)], True),
                       ("The hen is in the pot.", [("bed", 0.05, -0.18, 1.0), ("hen", 0, 0.3, 0.55)], False),
                       ("The sun is up.", [("hut", -0.4, -0.18, 0.75), ("sun", 0.45, 0.25, 0.55)], True)],
              "Week 4 · Day 20"),
        reading_check(20, T4, ["cat", "hat", "van", "map", "dog", "box", "pot", "mop", "pig", "lid", "pin", "six",
                               "bus", "sun", "cup", "bug", "bed", "hen", "net", "jet"], "Week 4 · Day 20"),
    ]
    all_words = ["cat", "hat", "rat", "bat", "van", "can", "fan", "pan", "map", "bag", "cap", "man",
                 "dog", "log", "box", "pot", "dot", "hot", "mop", "top", "pig", "wig", "dig", "lid",
                 "pin", "bin", "fin", "six", "bus", "sun", "cup", "bug", "nut", "rug", "tub", "hut",
                 "bed", "hen", "net", "pen", "jet", "web", "ten", "leg"]
    cards = [all_words[i:i + 12] for i in range(0, len(all_words), 12)]
    consonants = list("bcdfghjklmnprstvwxz") + list("bcdgmnpst")
    vowels = list("aeiou") * 3 + list("aeiou")

    story = [Page(cover)] + guide_story() + [Page(vowel_poster), Page(solar_chart)]
    names = {1: "short a", 2: "short o and i", 3: "short u and e", 4: "Read it!"}
    for wk, pages in zip((1, 2, 3, 4), (w1, w2, w3, w4)):
        story.append(Page(section_title(f"Week {wk}", names[wk], TH[wk])))
        story += [Page(f) for f in pages]
    story.append(Page(section_title("Cut-Outs & Games", "Word cards, letter tiles and Robot Bingo", TH["x"])))
    story += [Page(word_cards(ws, i + 1, len(cards))) for i, ws in enumerate(cards)]
    story += [Page(letter_tiles(consonants, "Letter Tiles: Consonants")),
              Page(letter_tiles(vowels, "Letter Tiles: Vowels (extra copies)")),
              Page(bingo()), Page(certificate)]
    story += key_story()
    build_pdf(OUT, f"{NAME}'s Word Workshop – 3-Letter Words", story)


if __name__ == "__main__":
    build()
