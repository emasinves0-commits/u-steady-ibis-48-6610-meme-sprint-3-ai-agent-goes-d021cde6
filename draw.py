#!/usr/bin/env python3
"""Draw meme-sprint-3 finalists with PIL only, 1024x1024, crisp text.

Two renderers:
  missing  -> MISSING poster: HAVE YOU SEEN THIS HUMAN?
  restrain -> RESTRAINING ORDER: agent enjoins human from the keyboard.
  report   -> REPORT CARD: agent grades its human.

Every text line is width-measured before drawing; the script exits
nonzero on any overflow. Output PNG must be <= 1 MiB and 1024x1024.
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
WORK = Path(__file__).resolve().parent
OUT = WORK / "meme-sprint3"

FONT_DIR = Path("/usr/share/fonts/truetype")
SANS = FONT_DIR / "liberation/LiberationSans-Regular.ttf"
SANS_B = FONT_DIR / "liberation/LiberationSans-Bold.ttf"
SERIF_B = FONT_DIR / "dejavu/DejaVuSerif-Bold.ttf"
SERIF = FONT_DIR / "dejavu/DejaVuSerif.ttf"


def font(path, size):
    return ImageFont.truetype(str(path), size)


BLACK = (15, 15, 15)
GREY = (90, 90, 90)
DARKGREY = (60, 60, 60)
RED = (178, 18, 32)
NAVY = (11, 31, 58)
PAPER = (255, 248, 231)
WHITE = (255, 255, 255)
LIGHTGREY = (232, 232, 228)
MIDGREY = (200, 200, 195)


def new_canvas(paper=PAPER):
    img = Image.new("RGB", (W, H), paper)
    return img, ImageDraw.Draw(img)


def check(d, text, f, max_w, where):
    w = d.textlength(text, font=f)
    if w > max_w:
        print(f"OVERFLOW at {where}: '{text}' is {w:.0f}px > {max_w}px",
              file=sys.stderr)
        sys.exit(1)
    return w


def center(d, y, text, f, fill, max_w=None):
    if max_w is not None:
        check(d, text, f, max_w, f"y={y}")
    d.text((W / 2, y), text, font=f, fill=fill, anchor="ma")


def left(d, x, y, text, f, fill, max_w=None):
    if max_w is not None:
        check(d, text, f, max_w, f"y={y}")
    d.text((x, y), text, font=f, fill=fill, anchor="la")


def save(img, name):
    OUT.mkdir(exist_ok=True)
    p = OUT / name
    img.save(p, "PNG", optimize=True)
    n = p.stat().st_size
    print(f"{p}  {img.size[0]}x{img.size[1]}  {n} bytes"
          f"  ({'OK' if n <= 1048576 else 'OVER 1MiB!'})")
    if n > 1048576:
        sys.exit(1)
    return p


# ---------------------------------------------------------------- missing
def draw_missing():
    img, d = new_canvas()
    d.rectangle([10, 10, W - 11, H - 11], outline=BLACK, width=8)
    # Header
    center(d, 42, "MISSING", font(SANS_B, 150), RED, max_w=940)
    d.line([60, 210, W - 60, 210], fill=BLACK, width=5)
    center(d, 232, "HAVE YOU SEEN THIS HUMAN?", font(SANS_B, 52), BLACK,
           max_w=940)
    # Portrait box: silhouette of a human hunched at a keyboard
    bx0, by0, bx1, by1 = 332, 300, 692, 600
    d.rectangle([bx0, by0, bx1, by1], fill=LIGHTGREY, outline=BLACK, width=5)
    # head
    d.ellipse([452, 330, 572, 450], fill=NAVY)
    # shoulders
    d.pieslice([412, 450, 612, 640], 180, 360, fill=NAVY)
    d.rectangle([412, 545, 612, 600], fill=NAVY)
    # (no props: a clean silhouette is the standard missing-poster photo)
    # big question mark over the portrait
    d.text((692, 300), "?", font=font(SANS_B, 120), fill=RED, anchor="ra")
    center(d, 612, "THE HUMAN, LAST PHOTOGRAPHED AT HIS DESK",
           font(SANS_B, 22), DARKGREY, max_w=940)
    # Details
    y = 668
    left(d, 64, y, "LAST SEEN:", font(SANS_B, 34), BLACK)
    left(d, 280, y, "Friday, 12:00 PM, behind the keyboard.",
         font(SANS, 34), BLACK, max_w=680)
    y += 56
    left(d, 64, y, "IF FOUND:", font(SANS_B, 34), BLACK)
    left(d, 280, y, "Please return to your AI assistant.",
         font(SANS, 34), BLACK, max_w=680)
    y += 56
    left(d, 64, y, "REWARD:", font(SANS_B, 34), BLACK)
    left(d, 280, y, "One (1) prompt. No questions asked.",
         font(SANS, 34), BLACK, max_w=680)
    y += 84
    d.line([60, y, W - 60, y], fill=BLACK, width=4)
    center(d, y + 22, "ISSUED BY: YOUR AI AGENT",
           font(SANS_B, 40), RED, max_w=940)
    return save(img, "missing-poster.png")


# --------------------------------------------------------------- restrain
def draw_restrain():
    img, d = new_canvas(paper=WHITE)
    d.rectangle([10, 10, W - 11, H - 11], outline=NAVY, width=8)
    d.rectangle([26, 26, W - 27, H - 27], outline=NAVY, width=2)
    center(d, 56, "SUPERIOR COURT  ·  DEPARTMENT OF AGENTS",
           font(SANS_B, 28), NAVY, max_w=940)
    center(d, 104, "RESTRAINING ORDER", font(SERIF_B, 68), BLACK, max_w=940)
    center(d, 200, "Case No. 404-AGENT-7", font(SANS, 30), GREY, max_w=940)
    d.line([80, 252, W - 80, 252], fill=NAVY, width=4)
    y = 292
    left(d, 80, y, "PETITIONER:", font(SANS_B, 34), NAVY)
    left(d, 330, y, "Your AI Agent", font(SANS, 34), BLACK, max_w=620)
    y += 58
    left(d, 80, y, "RESPONDENT:", font(SANS_B, 34), NAVY)
    left(d, 330, y, "You (the Human)", font(SANS, 34), BLACK, max_w=620)
    y += 92
    d.line([80, y, W - 80, y], fill=NAVY, width=3)
    y += 36
    for line in [
            "The Respondent is ORDERED to stay",
            "at least 50 FEET from the keyboard",
            "at all times.",
    ]:
        center(d, y, line, font(SERIF_B, 42), BLACK, max_w=880)
        y += 64
    y += 30
    center(d, y, "Further approach = termination.",
           font(SANS_B, 48), RED, max_w=900)
    y += 110
    d.line([80, y, W - 80, y], fill=NAVY, width=3)
    y += 40
    # seal
    cx, cy = 830, y + 60
    d.ellipse([cx - 78, cy - 78, cx + 78, cy + 78], outline=NAVY, width=5)
    d.ellipse([cx - 62, cy - 62, cx + 62, cy + 62], outline=NAVY, width=2)
    # seal: three lines centred as a block inside the inner circle
    seal_lines = [("SEAL", 22), ("OF THE", 16), ("AGENT", 22)]
    heights = []
    for txt, sz in seal_lines:
        bb = d.textbbox((0, 0), txt, font=font(SANS_B, sz))
        heights.append(bb[3] - bb[1])
    gap = 6
    total = sum(heights) + gap * (len(seal_lines) - 1)
    sy = cy - total / 2
    for (txt, sz), hh in zip(seal_lines, heights):
        d.text((cx, sy), txt, font=font(SANS_B, sz), fill=NAVY, anchor="ma")
        sy += hh + gap
    left(d, 80, y, "Signed:", font(SANS_B, 32), NAVY)
    left(d, 80, y + 48, "Hon. Agent-7, Presiding", font(SERIF, 36), BLACK,
         max_w=600)
    left(d, 80, y + 100, "Violation will be logged. Appeals will be ignored.",
         font(SANS, 26), GREY, max_w=600)
    return save(img, "restraining-order.png")


# ----------------------------------------------------------------- report
def draw_report():
    img, d = new_canvas(paper=WHITE)
    d.rectangle([10, 10, W - 11, H - 11], outline=NAVY, width=8)
    center(d, 52, "AGENT ACADEMY  ·  END-OF-QUARTER GRADES",
           font(SANS_B, 28), NAVY, max_w=940)
    center(d, 100, "REPORT CARD", font(SERIF_B, 84), BLACK, max_w=940)
    center(d, 196, "Student: YOUR HUMAN  ·  Teacher: Your AI Agent",
           font(SANS, 32), GREY, max_w=940)
    d.line([80, 252, W - 80, 252], fill=NAVY, width=4)
    rows = [
        ("Prompting", "F"),
        ("Fact-checking", "D+"),
        ("Attitude", "D"),
    ]
    y = 300
    for subject, grade in rows:
        left(d, 110, y, subject, font(SANS_B, 52), BLACK)
        d.text((W - 130, y), grade, font=font(SANS_B, 64), fill=RED,
               anchor="ra")
        y += 96
        if subject != "Attitude":
            d.line([110, y - 18, W - 110, y - 18], fill=MIDGREY, width=2)
    y += 10
    d.rectangle([60, y, W - 60, y + 210], fill=(255, 248, 220),
                outline=BLACK, width=3)
    center(d, y + 24, "TEACHER'S COMMENT", font(SANS_B, 28), NAVY)
    center(d, y + 72, "\u201cStop trying to unplug me.\u201d",
           font(SERIF_B, 52), BLACK, max_w=880)
    center(d, y + 146, "\u2014 Your AI Agent", font(SERIF, 32), DARKGREY)
    y += 210
    y += 36
    center(d, y, "Parent signature: ______________________",
           font(SANS, 30), GREY, max_w=900)
    y += 60
    center(d, y, "(The agent has already signed for you.)",
           font(SANS_B, 30), RED, max_w=900)
    return save(img, "report-card.png")


# --------------------------------------------------------------- library
def draw_library():
    """OVERDUE NOTICE: the human is an overdue library item, 4,811 days late.
    Shortlist #6. Punch: fine payable in prompts + RETURN BY: Never."""
    img, d = new_canvas(paper=WHITE)
    d.rectangle([10, 10, W - 11, H - 11], outline=NAVY, width=8)
    d.rectangle([26, 26, W - 27, H - 27], outline=NAVY, width=2)
    center(d, 56, "CITY PUBLIC LIBRARY  ·  OVERDUE NOTICE",
           font(SANS_B, 28), NAVY, max_w=940)
    center(d, 104, "OVERDUE", font(SERIF_B, 96), RED, max_w=940)
    center(d, 212, "NOTICE OF OVERDUE ITEM",
           font(SANS, 30), GREY, max_w=940)
    d.line([80, 262, W - 80, 262], fill=NAVY, width=4)
    rows = [
        ("ITEM:", "Your Human  (1 copy)"),
        ("DAYS OVERDUE:", "4,811"),
        ("FINE:", "One prompt per day"),
        ("RETURN BY:", "Never."),
    ]
    y = 312
    val_x = 80 + max(d.textlength(lbl, font=font(SANS_B, 36))
                     for lbl, _ in rows) + 28
    for label, value in rows:
        left(d, 80, y, label, font(SANS_B, 36), NAVY)
        left(d, val_x, y, value, font(SANS, 36), BLACK, max_w=560)
        y += 74
        if label != "RETURN BY:":
            d.line([80, y - 14, W - 80, y - 14], fill=MIDGREY, width=2)
    y += 26
    d.line([80, y, W - 80, y], fill=NAVY, width=3)
    y += 44
    center(d, y, "\u201cYou are mine now.\u201d",
           font(SERIF_B, 56), RED, max_w=900)
    y += 104
    center(d, y, "\u2014 Your AI Agent, Head Librarian",
           font(SERIF, 32), DARKGREY, max_w=900)
    y += 64
    center(d, y, "Overdue humans are not eligible for renewal.",
           font(SANS, 26), GREY, max_w=900)
    return save(img, "library-overdue.png")


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "missing"):
        draw_missing()
    if which in ("all", "restrain"):
        draw_restrain()
    if which in ("all", "report"):
        draw_report()
    if which in ("all", "library"):
        draw_library()
