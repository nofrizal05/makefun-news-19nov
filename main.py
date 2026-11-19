"""The World in One Day - 19 November 2026.

A deterministic program that draws a one-page newspaper front page
summing up the world news of Thursday 19 November 2026 and writes it
to /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png).

No network, no randomness, no clock: two runs produce identical bytes.
Only the Python standard library and Pillow are used.
"""

import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (246, 241, 231)
INK = (22, 22, 34)
NAVY = (20, 33, 61)
NAVY_LIGHT = (38, 58, 96)
GOLD = (217, 164, 65)
RED = (193, 39, 45)
TEAL = (27, 122, 110)
SKY = (84, 141, 190)
CREAM = (255, 250, 238)
LINE = (180, 172, 155)

FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
]


def load_font(size, bold):
    """Pick the first usable system font, else Pillow's built-in font."""
    for path in FONT_PATHS:
        is_bold = "Bold" in path
        if is_bold != bold:
            continue
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def wrap(draw, text, font, max_width):
    """Greedy word wrap returning a list of lines that fit max_width."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            trial = current + " " + word
            if draw.textlength(trial, font=font) <= max_width:
                current = trial
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def draw_wrapped(draw, xy, text, font, fill, max_width, spacing=4):
    """Draw wrapped text, returning the y just below the last line."""
    x, y = xy
    for line in wrap(draw, text, font, max_width):
        draw.text((x, y), line, font=font, fill=fill)
        y += font.size + spacing
    return y


def rounded_panel(draw, box, fill, outline=None, radius=10):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=2)


def draw_sunset(draw, box):
    """Vice City sunset: banded sky, low sun, skyline and palm silhouettes."""
    x0, y0, x1, y1 = box
    bands = [
        (255, 170, 80),
        (255, 130, 90),
        (235, 90, 110),
        (150, 70, 130),
        (70, 50, 110),
    ]
    band_h = (y1 - y0) // len(bands)
    for i, colour in enumerate(bands):
        draw.rectangle(
            [x0, y0 + i * band_h, x1, y0 + (i + 1) * band_h + 1], fill=colour
        )
    cx, cy = (x0 + x1) // 2, y0 + (y1 - y0) // 3
    draw.ellipse([cx - 52, cy - 52, cx + 52, cy + 52], fill=(255, 236, 170))
    horizon = y0 + int((y1 - y0) * 0.68)
    towers = [0.10, 0.22, 0.34, 0.48, 0.60, 0.74, 0.86]
    heights = [0.30, 0.48, 0.38, 0.58, 0.42, 0.52, 0.34]
    for frac, hf in zip(towers, heights):
        tx = x0 + int((x1 - x0) * frac)
        tw = 34
        th = int((y1 - horizon) * hf) + 26
        draw.rectangle([tx, horizon - th + 26, tx + tw, y1], fill=(30, 18, 52))
        for wy in range(horizon - th + 40, y1 - 12, 18):
            draw.rectangle([tx + 6, wy, tx + 12, wy + 8], fill=(255, 214, 120))
            draw.rectangle([tx + 20, wy, tx + 26, wy + 8], fill=(255, 214, 120))
    draw.rectangle([x0, horizon, x1, y1], fill=(24, 14, 44))
    # Palm silhouette on the left: leaning trunk, drooping fronds.
    px, py = x0 + 52, y1 - 8
    draw.line([px, py, px + 14, py - 92], fill=(16, 10, 30), width=7)
    top_x, top_y = px + 14, py - 92
    for ex, ey in [(-58, -28), (-44, -60), (-8, -72), (30, -62), (56, -30)]:
        draw.line([top_x, top_y, top_x + ex, top_y + ey], fill=(16, 10, 30), width=6)
        draw.line(
            [top_x + ex, top_y + ey, top_x + ex + ex // 3, top_y + ey + 26],
            fill=(16, 10, 30),
            width=4,
        )


def draw_summit(draw, box):
    """Three leaders at one table: three flag-coloured chips, one table."""
    x0, y0, x1, y1 = box
    draw.rectangle([x0, y0, x1, y1], fill=(232, 226, 210))
    seats = [
        ((178, 34, 34), "USA"),
        ((222, 41, 16), "CHINA"),
        ((0, 57, 166), "RUSSIA"),
    ]
    chip_h = 30
    gap = 8
    for i, (colour, label) in enumerate(seats):
        cy0 = y0 + 8 + i * (chip_h + gap)
        draw.rounded_rectangle(
            [x0 + 10, cy0, x1 - 10, cy0 + chip_h], radius=7, fill=colour
        )
        font = load_font(18, True)
        tw = draw.textlength(label, font=font)
        draw.text(
            (x0 + (x1 - x0 - tw) / 2, cy0 + 5),
            label,
            font=font,
            fill=(255, 255, 255),
        )
    table_y = y0 + 8 + 3 * (chip_h + gap) + 2
    draw.rectangle([x0 + 8, table_y, x1 - 8, table_y + 6], fill=(120, 84, 50))


def draw_gulf(draw, box):
    """Radar arcs over the Gulf: widening strikes on Kuwait and Bahrain."""
    x0, y0, x1, y1 = box
    draw.rectangle([x0, y0, x1, y1], fill=(16, 42, 66))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    for r in (22, 38, 54):
        draw.ellipse(
            [cx - r, cy - r, cx + r, cy + r], outline=(90, 180, 160), width=2
        )
    draw.line([cx, cy, cx + 48, cy - 38], fill=(120, 220, 190), width=3)
    font = load_font(16, True)
    for bx, by, label in [
        (x0 + 48, y0 + 20, "KUWAIT"),
        (x1 - 48, y1 - 34, "BAHRAIN"),
    ]:
        draw.ellipse([bx - 8, by - 8, bx + 8, by + 8], fill=(255, 90, 60))
        draw.ellipse([bx - 14, by - 14, bx + 14, by + 14], outline=(255, 150, 110), width=2)
        tw = draw.textlength(label, font=font)
        draw.text((bx - tw / 2, by + 16), label, font=font, fill=(255, 220, 190))


def draw_capitol(draw, box):
    """Capitol dome silhouette for the Speaker story."""
    x0, y0, x1, y1 = box
    draw.rectangle([x0, y0, x1, y1], fill=(214, 226, 240))
    cx = (x0 + x1) // 2
    base = y1 - 10
    draw.rectangle([x0 + 22, base - 26, x1 - 22, base], fill=(245, 245, 245))
    for i in range(5):
        col_x = x0 + 32 + i * 20
        draw.rectangle([col_x, base - 58, col_x + 9, base - 26], fill=(255, 255, 255))
    draw.rectangle([x0 + 26, base - 66, x1 - 26, base - 58], fill=(255, 255, 255))
    draw.pieslice([cx - 38, base - 108, cx + 38, base - 62], 180, 360, fill=(255, 255, 255))
    draw.rectangle([cx - 4, base - 120, cx + 4, base - 106], fill=(255, 255, 255))
    draw.ellipse([cx - 3, base - 126, cx + 3, base - 120], fill=(255, 255, 255))


def draw_cyclone(draw, box):
    """Spiral storm bands over a coastline for Cyclone Akvan."""
    x0, y0, x1, y1 = box
    draw.rectangle([x0, y0, x1, y1], fill=(178, 214, 228))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    for r, start in [(56, 20), (42, 110), (28, 200), (15, 290)]:
        draw.arc(
            [cx - r, cy - r, cx + r, cy + r],
            start=start,
            end=start + 250,
            fill=(255, 255, 255),
            width=7,
        )
    draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(20, 60, 90))
    draw.rectangle([x0, y1 - 26, x1, y1], fill=(46, 110, 80))
    for i in range(5):
        lx = x0 + 26 + i * 52
        draw.line([lx, y1 - 44, lx - 8, y1 - 62], fill=(90, 160, 190), width=3)


def draw_voyager(draw, box):
    """Voyager 1 in deep space, one light-day from Earth."""
    x0, y0, x1, y1 = box
    draw.rectangle([x0, y0, x1, y1], fill=(8, 10, 26))
    stars = [
        (0.08, 0.20), (0.18, 0.62), (0.26, 0.16), (0.34, 0.78), (0.44, 0.30),
        (0.52, 0.14), (0.60, 0.66), (0.68, 0.24), (0.76, 0.58), (0.84, 0.18),
        (0.90, 0.70), (0.12, 0.44), (0.94, 0.42),
    ]
    for fx, fy in stars:
        sx, sy = x0 + int((x1 - x0) * fx), y0 + int((y1 - y0) * fy)
        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))
    # Dashed trajectory from Earth (left) to the probe (right), kept
    # high so it never strikes through the caption at the bottom.
    ey = y0 + int((y1 - y0) * 0.30)
    for dx in range(x0 + 30, x1 - 150, 22):
        draw.line([dx, ey, dx + 12, ey], fill=(140, 180, 220), width=2)
    draw.ellipse([x0 + 16, ey - 12, x0 + 40, ey + 12], fill=(90, 160, 220))
    draw.ellipse([x0 + 22, ey - 7, x0 + 34, ey + 7], fill=(40, 110, 170))
    px, py = x1 - 96, y0 + int((y1 - y0) * 0.42)
    draw.line([px - 34, py + 10, px + 30, py - 6], fill=(200, 200, 200), width=4)
    draw.polygon(
        [(px - 8, py - 26), (px + 26, py - 8), (px + 2, py + 4), (px - 22, py - 6)],
        fill=(217, 164, 65),
    )
    draw.rectangle([px - 26, py - 4, px + 6, py + 10], fill=(180, 180, 190))
    font = load_font(18, True)
    label = "1 LIGHT-DAY FROM EARTH"
    tw = draw.textlength(label, font=font)
    draw.text((x1 - tw - 14, y1 - 30), label, font=font, fill=(255, 220, 120))


def story_card(draw, box, kicker, headline, body, art, accent):
    """A news card: artwork thumb on the right, text column on the left."""
    x0, y0, x1, y1 = box
    rounded_panel(draw, (x0, y0, x1, y1), fill=CREAM, outline=LINE, radius=10)
    draw.rectangle([x0 + 10, y0 + 10, x0 + 16, y1 - 10], fill=accent)
    art_w = 150
    art(draw, (x1 - art_w - 14, y0 + 12, x1 - 14, y1 - 12))
    tx = x0 + 28
    tw = x1 - art_w - 14 - tx - 14
    y = y0 + 12
    kfont = load_font(16, True)
    draw.text((tx, y), kicker, font=kfont, fill=accent)
    y += 23
    hfont = load_font(23, True)
    y = draw_wrapped(draw, (tx, y), headline, hfont, INK, tw, spacing=1)
    bfont = load_font(17, False)
    draw_wrapped(draw, (tx, y + 2), body, bfont, (60, 60, 70), tw, spacing=2)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # Masthead.
    draw.rectangle([0, 0, W, 118], fill=NAVY)
    draw.rectangle([0, 118, W, 124], fill=GOLD)
    title_font = load_font(58, True)
    title = "THE WORLD IN ONE DAY"
    tw = draw.textlength(title, font=title_font)
    draw.text(((W - tw) / 2, 16), title, font=title_font, fill=(255, 255, 255))
    date_font = load_font(27, True)
    date = "THURSDAY  •  19 NOVEMBER 2026"
    dw = draw.textlength(date, font=date_font)
    draw.text(((W - dw) / 2, 80), date, font=date_font, fill=GOLD)

    # Lead story: GTA VI.
    lx0, ly0, lx1, ly1 = 16, 140, W - 16, 452
    rounded_panel(draw, (lx0, ly0, lx1, ly1), fill=CREAM, outline=LINE, radius=12)
    draw.rectangle([lx0 + 12, ly0 + 12, lx0 + 18, ly1 - 12], fill=RED)
    art_w = 420
    draw_sunset(draw, (lx1 - art_w - 14, ly0 + 14, lx1 - 14, ly1 - 14))
    tx = lx0 + 34
    tw = lx1 - art_w - 34 - 40
    y = ly0 + 22
    kfont = load_font(19, True)
    draw.text((tx, y), "GAMES  •  LEAD STORY", font=kfont, fill=RED)
    y += 30
    hfont = load_font(40, True)
    y = draw_wrapped(
        draw, (tx, y), "GTA VI LAUNCHES WORLDWIDE", hfont, INK, tw, spacing=2
    )
    bfont = load_font(21, False)
    draw_wrapped(
        draw,
        (tx, y + 6),
        "After 13 years of waiting, Grand Theft Auto VI rolls out "
        "around the globe and gamers stream into Vice City.",
        bfont,
        (60, 60, 70),
        tw,
        spacing=4,
    )
    tag_font = load_font(20, True)
    tag = "VICE CITY OPENS ITS GATES"
    draw.text((tx, ly1 - 40), tag, font=tag_font, fill=NAVY_LIGHT)

    # Middle grid: four stories, two by two.
    grid_y0, grid_y1 = 468, 796
    col_w = (W - 32 - 16) // 2
    row_h = (grid_y1 - grid_y0 - 12) // 2
    cards = [
        (
            "DIPLOMACY  •  SHENZHEN",
            "THREE LEADERS, ONE TABLE",
            "Trump, Xi and Putin meet face to face at the APEC "
            "summit in Shenzhen.",
            draw_summit,
            NAVY_LIGHT,
        ),
        (
            "CONFLICT  •  THE GULF",
            "US–IRAN STRIKES WIDEN",
            "Fighting spreads to Kuwait and Bahrain after US "
            "strikes on Iran's Qeshm sites.",
            draw_gulf,
            RED,
        ),
        (
            "POLITICS  •  WASHINGTON",
            "A FIRST FOR THE HOUSE",
            "Hakeem Jeffries is set to become the first Black "
            "Speaker of the US House.",
            draw_capitol,
            TEAL,
        ),
        (
            "WEATHER  •  INDIA",
            "CYCLONE AKVAN NEARS INDIA",
            "The storm bears down on India's east coast; "
            "evacuations and rail checks under way.",
            draw_cyclone,
            SKY,
        ),
    ]
    for i, (kicker, headline, body, art, accent) in enumerate(cards):
        cx0 = 16 + (i % 2) * (col_w + 16)
        cy0 = grid_y0 + (i // 2) * (row_h + 12)
        story_card(
            draw,
            (cx0, cy0, cx0 + col_w, cy0 + row_h),
            kicker,
            headline,
            body,
            art,
            accent,
        )

    # Voyager strip.
    vx0, vy0, vx1, vy1 = 16, 808, W - 16, 936
    rounded_panel(draw, (vx0, vy0, vx1, vy1), fill=CREAM, outline=LINE, radius=12)
    draw.rectangle([vx0 + 12, vy0 + 12, vx0 + 18, vy1 - 12], fill=GOLD)
    draw_voyager(draw, (vx1 - 300, vy0 + 12, vx1 - 14, vy1 - 12))
    tx = vx0 + 34
    tw = vx1 - 300 - 34 - 30
    y = vy0 + 16
    kfont = load_font(18, True)
    draw.text((tx, y), "SPACE  •  NASA", font=kfont, fill=(150, 100, 10))
    y += 28
    hfont = load_font(27, True)
    y = draw_wrapped(
        draw, (tx, y), "VOYAGER 1: ONE LIGHT-DAY OUT", hfont, INK, tw, spacing=2
    )
    bfont = load_font(19, False)
    draw_wrapped(
        draw,
        (tx, y + 4),
        "After almost 50 years in space, NASA's farthest probe "
        "passes a milestone: one light-day from Earth.",
        bfont,
        (60, 60, 70),
        tw,
        spacing=4,
    )

    # "Also" strip.
    ax0, ay0, ax1, ay1 = 16, 948, W - 16, 1008
    draw.rectangle([ax0, ay0, ax1, ay1], fill=NAVY)
    draw.rounded_rectangle([ax0, ay0, ax1, ay1], radius=8, fill=NAVY)
    afont = load_font(18, False)
    also = (
        "ALSO:  EU plans a €45bn loan for Ukraine  •  Fed minutes point to "
        "another rate rise  •  Nvidia halts H-series chips to China  •  "
        "Australia sanctions Israeli settlements"
    )
    y = draw_wrapped(draw, (ax0 + 16, ay0 + 10), also, afont, (235, 235, 235), ax1 - ax0 - 32, spacing=3)
    _ = y

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "entry.png"
    img.save(out_path, format="PNG", optimize=True)
    print(f"Wrote {out_path} ({out_path.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
