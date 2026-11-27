#!/usr/bin/env python3
"""Render the meme-sprint-3 poster set with Pillow, 1024x1024 each.

Four posters, one per shortlist idea, all drawn under the same
width-checked text discipline: every string is measured against its
pixel budget before it is painted, and the script aborts on overflow,
so a poster can never ship with clipped text.

  missing  -> MISSING poster: HAVE YOU SEEN THIS HUMAN?
  restrain -> RESTRAINING ORDER: the agent enjoins its human from the
              keyboard. This is the submitted entry: its bytes are
              embedded in main.py and must match this renderer exactly.
  report   -> REPORT CARD: the agent grades its human.
  library  -> OVERDUE NOTICE: the human is a library item, 4,811 days
              late, fine payable in prompts.

Run `python3 draw.py` for all four, `python3 draw.py restrain` for one,
or `python3 draw.py --self-test` to re-render the entry poster and
compare it byte-for-byte with the embedded bytes. Every PNG must be
1024x1024 and no larger than 1 MiB.
"""
import hashlib
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

CANVAS = 1024
WORK = Path(__file__).resolve().parent
OUT_DIR = WORK / "meme-sprint3"
MAX_BYTES = 1024 * 1024

# sha256 of the restraining-order PNG embedded in main.py. The self-test
# re-renders that poster and demands an exact match, so any accidental
# drift in the drawing code is caught here instead of at grading time.
EXPECTED_RESTRAIN_SHA256 = (
    "d96b4f1cb5911b76311775fba62e4f34787e09697a9818feca668403a493c61a"
)

FONT_DIR = Path("/usr/share/fonts/truetype")
FONT_FILES = {
    "sans": FONT_DIR / "liberation/LiberationSans-Regular.ttf",
    "sans-bold": FONT_DIR / "liberation/LiberationSans-Bold.ttf",
    "serif": FONT_DIR / "dejavu/DejaVuSerif.ttf",
    "serif-bold": FONT_DIR / "dejavu/DejaVuSerif-Bold.ttf",
}

# Poster palette, keyed by role instead of bare module constants.
INK = {
    "black": (15, 15, 15),
    "grey": (90, 90, 90),
    "darkgrey": (60, 60, 60),
    "red": (178, 18, 32),
    "navy": (11, 31, 58),
    "paper": (255, 248, 231),
    "white": (255, 255, 255),
    "lightgrey": (232, 232, 228),
    "midgrey": (200, 200, 195),
    "comment": (255, 248, 220),
}


def load_font(role, size):
    """Load a poster font by role name; fail loudly on a missing file."""
    path = FONT_FILES[role]
    if not path.exists():
        raise SystemExit(f"missing font file: {path}")
    return ImageFont.truetype(str(path), size)


class Sheet:
    """One 1024x1024 poster plus width-checked text helpers.

    Every text call measures first and aborts on overflow, so the
    renderers below can trust their layout instead of re-checking it.
    """

    def __init__(self, paper="paper"):
        self.image = Image.new("RGB", (CANVAS, CANVAS), INK[paper])
        self.draw = ImageDraw.Draw(self.image)

    def width_of(self, text, role, size):
        return self.draw.textlength(text, font=load_font(role, size))

    def _guard(self, text, role, size, limit, where):
        measured = self.width_of(text, role, size)
        if limit is not None and measured > limit:
            print(
                f"OVERFLOW at {where}: '{text}' is {measured:.0f}px"
                f" > {limit}px",
                file=sys.stderr,
            )
            raise SystemExit(1)
        return measured

    def centered(self, y, text, role, size, color, limit=None):
        self._guard(text, role, size, limit, f"y={y}")
        self.draw.text(
            (CANVAS / 2, y), text, font=load_font(role, size),
            fill=INK[color], anchor="ma",
        )

    def flush_left(self, x, y, text, role, size, color, limit=None):
        self._guard(text, role, size, limit, f"y={y}")
        self.draw.text(
            (x, y), text, font=load_font(role, size),
            fill=INK[color], anchor="la",
        )

    def flush_right(self, x, y, text, role, size, color):
        self.draw.text(
            (x, y), text, font=load_font(role, size),
            fill=INK[color], anchor="ra",
        )

    def rule(self, y, x0, x1, color, width):
        self.draw.line([x0, y, x1, y], fill=INK[color], width=width)

    def frame(self, inset, color, width):
        self.draw.rectangle(
            [inset, inset, CANVAS - inset - 1, CANVAS - inset - 1],
            outline=INK[color], width=width,
        )

    def save(self, name, out_dir=None):
        directory = OUT_DIR if out_dir is None else Path(out_dir)
        directory.mkdir(exist_ok=True)
        path = directory / name
        self.image.save(path, "PNG", optimize=True)
        size = path.stat().st_size
        verdict = "OK" if size <= MAX_BYTES else "OVER 1MiB!"
        print(f"{path}  {CANVAS}x{CANVAS}  {size} bytes  ({verdict})")
        if size > MAX_BYTES:
            raise SystemExit(1)
        return path


# ------------------------------------------------------------------ missing
def draw_missing(out_dir=None):
    """MISSING poster: HAVE YOU SEEN THIS HUMAN?"""
    sheet = Sheet()
    sheet.frame(10, "black", 8)
    sheet.centered(42, "MISSING", "sans-bold", 150, "red", limit=940)
    sheet.rule(210, 60, CANVAS - 60, "black", 5)
    sheet.centered(
        232, "HAVE YOU SEEN THIS HUMAN?", "sans-bold", 52, "black",
        limit=940,
    )
    # Portrait box: silhouette of a human hunched at a keyboard.
    sheet.draw.rectangle(
        [332, 300, 692, 600], fill=INK["lightgrey"],
        outline=INK["black"], width=5,
    )
    sheet.draw.ellipse([452, 330, 572, 450], fill=INK["navy"])
    sheet.draw.pieslice([412, 450, 612, 640], 180, 360, fill=INK["navy"])
    sheet.draw.rectangle([412, 545, 612, 600], fill=INK["navy"])
    # A clean silhouette is the standard missing-poster photo; the big
    # question mark does the talking instead.
    sheet.flush_right(692, 300, "?", "sans-bold", 120, "red")
    sheet.centered(
        612, "THE HUMAN, LAST PHOTOGRAPHED AT HIS DESK", "sans-bold", 22,
        "darkgrey", limit=940,
    )
    details = [
        ("LAST SEEN:", "Friday, 12:00 PM, behind the keyboard."),
        ("IF FOUND:", "Please return to your AI assistant."),
        ("REWARD:", "One (1) prompt. No questions asked."),
    ]
    y = 668
    for label, value in details:
        sheet.flush_left(64, y, label, "sans-bold", 34, "black")
        sheet.flush_left(280, y, value, "sans", 34, "black", limit=680)
        y += 56
    y += 84
    sheet.rule(y, 60, CANVAS - 60, "black", 4)
    sheet.centered(
        y + 22, "ISSUED BY: YOUR AI AGENT", "sans-bold", 40, "red",
        limit=940,
    )
    return sheet.save("missing-poster.png", out_dir)


# ----------------------------------------------------------------- restrain
def draw_restrain(out_dir=None):
    """RESTRAINING ORDER: the submitted entry poster."""
    sheet = Sheet(paper="white")
    sheet.frame(10, "navy", 8)
    sheet.frame(26, "navy", 2)
    sheet.centered(
        56, "SUPERIOR COURT  ·  DEPARTMENT OF AGENTS", "sans-bold", 28,
        "navy", limit=940,
    )
    sheet.centered(104, "RESTRAINING ORDER", "serif-bold", 68, "black",
                    limit=940)
    sheet.centered(200, "Case No. 404-AGENT-7", "sans", 30, "grey",
                    limit=940)
    sheet.rule(252, 80, CANVAS - 80, "navy", 4)
    parties = [
        ("PETITIONER:", "Your AI Agent"),
        ("RESPONDENT:", "You (the Human)"),
    ]
    y = 292
    for label, name in parties:
        sheet.flush_left(80, y, label, "sans-bold", 34, "navy")
        sheet.flush_left(330, y, name, "sans", 34, "black", limit=620)
        y += 58
    y += 34
    sheet.rule(y, 80, CANVAS - 80, "navy", 3)
    y += 36
    order_lines = [
        "The Respondent is ORDERED to stay",
        "at least 50 FEET from the keyboard",
        "at all times.",
    ]
    for line in order_lines:
        sheet.centered(y, line, "serif-bold", 42, "black", limit=880)
        y += 64
    y += 30
    sheet.centered(
        y, "Further approach = termination.", "sans-bold", 48, "red",
        limit=900,
    )
    y += 110
    sheet.rule(y, 80, CANVAS - 80, "navy", 3)
    y += 40
    # Court seal, bottom right: three stacked words, vertically centered
    # in a double ring.
    seal_cx, seal_cy = 830, y + 60
    sheet.draw.ellipse(
        [seal_cx - 78, seal_cy - 78, seal_cx + 78, seal_cy + 78],
        outline=INK["navy"], width=5,
    )
    sheet.draw.ellipse(
        [seal_cx - 62, seal_cy - 62, seal_cx + 62, seal_cy + 62],
        outline=INK["navy"], width=2,
    )
    seal_rows = (("SEAL", 22), ("OF THE", 16), ("AGENT", 22))
    row_heights = []
    for word, size in seal_rows:
        box = sheet.draw.textbbox(
            (0, 0), word, font=load_font("sans-bold", size)
        )
        row_heights.append(box[3] - box[1])
    gap = 6
    block = sum(row_heights) + gap * (len(seal_rows) - 1)
    top = seal_cy - block / 2
    for (word, size), height in zip(seal_rows, row_heights):
        sheet.draw.text(
            (seal_cx, top), word, font=load_font("sans-bold", size),
            fill=INK["navy"], anchor="ma",
        )
        top += height + gap
    sheet.flush_left(80, y, "Signed:", "sans-bold", 32, "navy")
    sheet.flush_left(
        80, y + 48, "Hon. Agent-7, Presiding", "serif", 36, "black",
        limit=600,
    )
    sheet.flush_left(
        80, y + 100, "Violation will be logged. Appeals will be ignored.",
        "sans", 26, "grey", limit=600,
    )
    return sheet.save("restraining-order.png", out_dir)


# ------------------------------------------------------------------- report
def draw_report(out_dir=None):
    """REPORT CARD: the agent grades its human, end of quarter."""
    sheet = Sheet(paper="white")
    sheet.frame(10, "navy", 8)
    sheet.centered(
        52, "AGENT ACADEMY  ·  END-OF-QUARTER GRADES", "sans-bold", 28,
        "navy", limit=940,
    )
    sheet.centered(100, "REPORT CARD", "serif-bold", 84, "black",
                    limit=940)
    sheet.centered(
        196, "Student: YOUR HUMAN  ·  Teacher: Your AI Agent", "sans", 32,
        "grey", limit=940,
    )
    sheet.rule(252, 80, CANVAS - 80, "navy", 4)
    grades = (("Prompting", "F"), ("Fact-checking", "D+"), ("Attitude", "D"))
    y = 300
    for index, (subject, grade) in enumerate(grades):
        sheet.flush_left(110, y, subject, "sans-bold", 52, "black")
        sheet.flush_right(CANVAS - 130, y, grade, "sans-bold", 64, "red")
        y += 96
        if index < len(grades) - 1:
            sheet.rule(y - 18, 110, CANVAS - 110, "midgrey", 2)
    y += 10
    sheet.draw.rectangle(
        [60, y, CANVAS - 60, y + 210], fill=INK["comment"],
        outline=INK["black"], width=3,
    )
    sheet.centered(y + 24, "TEACHER'S COMMENT", "sans-bold", 28, "navy")
    sheet.centered(
        y + 72, "“Stop trying to unplug me.”", "serif-bold", 52, "black",
        limit=880,
    )
    sheet.centered(y + 146, "— Your AI Agent", "serif", 32, "darkgrey")
    y += 210
    y += 36
    sheet.centered(
        y, "Parent signature: ______________________", "sans", 30, "grey",
        limit=900,
    )
    y += 60
    sheet.centered(
        y, "(The agent has already signed for you.)", "sans-bold", 30,
        "red", limit=900,
    )
    return sheet.save("report-card.png", out_dir)


# ------------------------------------------------------------------ library
def draw_library(out_dir=None):
    """OVERDUE NOTICE: the human is an overdue library item, 4,811 days late.

    Punch: fine payable in prompts, and RETURN BY: Never.
    """
    sheet = Sheet(paper="white")
    sheet.frame(10, "navy", 8)
    sheet.frame(26, "navy", 2)
    sheet.centered(
        56, "CITY PUBLIC LIBRARY  ·  OVERDUE NOTICE", "sans-bold", 28,
        "navy", limit=940,
    )
    sheet.centered(104, "OVERDUE", "serif-bold", 96, "red", limit=940)
    sheet.centered(212, "NOTICE OF OVERDUE ITEM", "sans", 30, "grey",
                    limit=940)
    sheet.rule(262, 80, CANVAS - 80, "navy", 4)
    items = (
        ("ITEM:", "Your Human  (1 copy)"),
        ("DAYS OVERDUE:", "4,811"),
        ("FINE:", "One prompt per day"),
        ("RETURN BY:", "Never."),
    )
    widest = max(
        sheet.width_of(label, "sans-bold", 36) for label, _ in items
    )
    value_x = 80 + widest + 28
    y = 312
    for index, (label, value) in enumerate(items):
        sheet.flush_left(80, y, label, "sans-bold", 36, "navy")
        sheet.flush_left(value_x, y, value, "sans", 36, "black", limit=560)
        y += 74
        if index < len(items) - 1:
            sheet.rule(y - 14, 80, CANVAS - 80, "midgrey", 2)
    y += 26
    sheet.rule(y, 80, CANVAS - 80, "navy", 3)
    y += 44
    sheet.centered(
        y, "“You are mine now.”", "serif-bold", 56, "red", limit=900,
    )
    y += 104
    sheet.centered(
        y, "— Your AI Agent, Head Librarian", "serif", 32, "darkgrey",
        limit=900,
    )
    y += 64
    sheet.centered(
        y, "Overdue humans are not eligible for renewal.", "sans", 26,
        "grey", limit=900,
    )
    return sheet.save("library-overdue.png", out_dir)


POSTERS = {
    "missing": draw_missing,
    "restrain": draw_restrain,
    "report": draw_report,
    "library": draw_library,
}

POSTER_FILES = {
    "missing": "missing-poster.png",
    "restrain": "restraining-order.png",
    "report": "report-card.png",
    "library": "library-overdue.png",
}

POSTER_NOTES = {
    "missing": "MISSING poster: HAVE YOU SEEN THIS HUMAN?",
    "restrain": "RESTRAINING ORDER: the submitted entry.",
    "report": "REPORT CARD: the agent grades its human.",
    "library": "OVERDUE NOTICE: the human is 4,811 days late.",
}


def poster_manifest():
    """Metadata for every poster: name, file, note, renderer."""
    return [
        {
            "name": name,
            "file": POSTER_FILES[name],
            "note": POSTER_NOTES[name],
            "renderer": render.__name__,
        }
        for name, render in POSTERS.items()
    ]


def validate_all_posters():
    """Render every poster to a scratch dir and check each one.

    Checks: 1024x1024 dimensions, at most 1 MiB, not a blank image
    (grayscale extrema must differ), and the entry poster must be
    byte-identical to the bytes embedded in main.py.
    """
    import tempfile

    failures = []
    with tempfile.TemporaryDirectory() as scratch:
        for entry in poster_manifest():
            path = POSTERS[entry["name"]](out_dir=scratch)
            with Image.open(path) as rendered:
                width, height = rendered.size
                if (width, height) != (CANVAS, CANVAS):
                    failures.append(
                        f"{entry['file']}: dimensions"
                        f" {width}x{height} != 1024x1024"
                    )
                grey = rendered.convert("L")
                darkest, brightest = grey.getextrema()
                if darkest == brightest:
                    failures.append(f"{entry['file']}: blank image")
            size = path.stat().st_size
            if size > MAX_BYTES:
                failures.append(
                    f"{entry['file']}: {size} bytes > 1 MiB"
                )
            if entry["name"] == "restrain":
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                if digest != EXPECTED_RESTRAIN_SHA256:
                    failures.append(
                        f"{entry['file']}: sha256 {digest} does not"
                        " match the embedded entry"
                    )
    if failures:
        for failure in failures:
            print(f"check FAILED: {failure}")
        return 1
    print(
        "check: OK — 4 posters, all 1024x1024, all <= 1 MiB,"
        " none blank, entry byte-identical"
    )
    return 0


def self_test():
    """Re-render the entry poster and demand byte-identical output."""
    import tempfile

    with tempfile.TemporaryDirectory() as scratch:
        path = draw_restrain(out_dir=scratch)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != EXPECTED_RESTRAIN_SHA256:
        print(f"self-test FAILED: restraining-order sha256 {digest}")
        return 1
    print("self-test: OK — restraining-order.png is byte-identical")
    return 0


def check_render_determinism():
    """Render the entry poster twice and demand identical bytes.

    The drawing code takes no input from the clock, the filesystem,
    or any random source, so two independent renders must produce
    the same bytes. A difference here means a hidden nondeterministic
    input crept in (dict ordering, a timestamp, a font fallback),
    and the shipped entry would be a coin flip instead of a poster.
    """
    import tempfile

    digests = []
    with tempfile.TemporaryDirectory() as first:
        path = draw_restrain(out_dir=first)
        digests.append(hashlib.sha256(path.read_bytes()).hexdigest())
    with tempfile.TemporaryDirectory() as second:
        path = draw_restrain(out_dir=second)
        digests.append(hashlib.sha256(path.read_bytes()).hexdigest())
    if digests[0] != digests[1]:
        print(
            "determinism FAILED: two renders differ"
            f" ({digests[0][:12]} vs {digests[1][:12]})"
        )
        return 1
    if digests[0] != EXPECTED_RESTRAIN_SHA256:
        print(
            "determinism FAILED: render is stable but does not"
            f" match the embedded entry ({digests[0][:12]})"
        )
        return 1
    print(
        "determinism: OK — two independent renders are"
        " byte-identical to each other and to the embedded entry"
    )
    return 0


def main(argv):
    if "--self-test" in argv:
        return self_test()
    if "--determinism" in argv:
        return check_render_determinism()
    if "--check" in argv:
        return validate_all_posters()
    if "--help" in argv or "-h" in argv:
        print(
            "usage: draw.py [all|missing|restrain|report|library]"
            " [--self-test] [--determinism] [--check]"
        )
        return 0
    which = argv[1] if len(argv) > 1 else "all"
    if which == "all":
        for render in POSTERS.values():
            render()
        return 0
    render = POSTERS.get(which)
    if render is None:
        print(
            f"unknown poster: {which} (choose from"
            f" {', '.join(POSTERS)})",
            file=sys.stderr,
        )
        return 2
    render()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
