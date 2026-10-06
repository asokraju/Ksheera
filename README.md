# Ksheera — printable learn & practice books

Kid-friendly math books to print at home. Each book has a parent guide (what to do and say),
worksheets, reprintable extra practice, a tracker, a certificate and an answer key.

## Books

| Grade | Book | PDF | Pages |
|---|---|---|---|
| 3rd | Multiplication Mastery — 4-week plan | [grade3/multiplication](grade3/multiplication/Multiplication_Mastery_Grade3.pdf) | 52 |
| 3rd | Division Made Easy — learn it today + 10 days practice | [grade3/division](grade3/division/Division_Made_Easy_Grade3.pdf) | 37 |
| K | *(coming next)* | [kindergarten/](kindergarten/) | |

## Layout

```
common/printkit.py      shared fonts, page layout, drawing & problem helpers (used by every book)
grade3/<topic>/         build.py + the generated PDF + README
kindergarten/<topic>/   same pattern
build_all.py            rebuild every book
```

## Building

Needs Python 3 and `reportlab` (`pip install reportlab`) plus the DejaVu Sans font
(set `KID_FONT_DIR` if it isn't in `/usr/share/fonts/truetype/dejavu/`).

```
python3 build_all.py                       # every book
python3 grade3/division/build.py           # one book
```

Problems use fixed random seeds, so a rebuild gives the same pages and the answer key always matches.

## Adding a new book

1. Make a folder `<grade>/<topic>/` with a `build.py` (copy the closest existing one as a template).
2. `from common.printkit import *`, write page functions `def draw(c, W, H)` and wrap them in `Page(...)`.
3. Append `(title, [answers])` to `KEY` for every page that has answers, and end the story with `key_story()`.
4. Call `build_pdf(OUT, title, story)`, add a short README, and list the book in the table above.
