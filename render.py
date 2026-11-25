#!/usr/bin/env python3
"""Render the news-image-20261125 entry image (build-time only).

Draws a 1024x1024 newspaper front page for Wednesday 25 November 2026
with PIL: every word is real text rendered from fonts on this machine,
nothing is baked into a generated picture. The output entry.png is
committed to the repository; the entry program (main.py) only copies it
to /output/entry.png at grading time. No network is used anywhere.

News selection (all first reported on 25 November 2026):
  1. China investigates Politburo member Chen Jining, Shanghai party
     chief (Reuters / Channel NewsAsia / Japan Times, 25 Nov)
  2. US jury convicts Huawei of stealing trade secrets (AP, 25 Nov)
  3. Nvidia's Jensen Huang says he is in therapy, a day after being
     reinstated as CEO; shares slide (SCMP, 25 Nov)
  4. Trump pardons the Thanksgiving turkeys at the White House
     (Manila Times / AP, 25 Nov)
  5. Gunmen take 25 hostage at a supermarket in Colombia (AP, 25 Nov)
  6. Saudi Arabia condemns a "terrorist attack" after the Riyadh PIF
     skyscraper is hit twice in a week (SCMP, 25 Nov)
  7. Five women killed every hour by relatives in 2025, UN says
     (Manila Times / UN, 25 Nov)
"""

import hashlib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 48
RIGHT = W - MARGIN

PAPER = (250, 246, 236)
INK = (24, 30, 52)
FAINT = (110, 104, 92)
NAVY = (23, 58, 94)
BAND_TEXT = (250, 246, 236)
GOLD = (198, 152, 52)
RULE = (216, 208, 190)

SERIF_BOLD = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SANS_BLACK = "/usr/share/fonts/truetype/noto/NotoSans-Black.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def centered(draw, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text(((W - w) / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size


def fit(draw, text, path, size, max_w):
    """Largest font size at or below `size` that fits `max_w`."""
    while size > 10 and draw.textlength(text, font=font(path, size)) > max_w:
        size -= 1
    return font(path, size)


def chip(draw, x, y, text, color, fnt):
    w = draw.textlength(text, font=fnt)
    pad_x, pad_y = 10, 4
    draw.rounded_rectangle(
        [x, y, x + w + 2 * pad_x, y + fnt.size + 2 * pad_y],
        radius=6,
        fill=color,
    )
    draw.text((x + pad_x, y + pad_y - 2), text, font=fnt, fill=(255, 255, 255))
    return y + fnt.size + 2 * pad_y


def badge(draw, cx, cy, num, color):
    d = draw
    d.ellipse([cx - 25, cy - 25, cx + 25, cy + 25], fill=color)
    nf = font(SANS_BOLD, 26)
    bb = d.textbbox((0, 0), num, font=nf)
    d.text(
        (cx - (bb[2] - bb[0]) / 2 - bb[0], cy - (bb[3] - bb[1]) / 2 - bb[1]),
        num,
        font=nf,
        fill=(255, 255, 255),
    )


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead ---------------------------------------------------
    d.rectangle([MARGIN, 26, RIGHT, 32], fill=INK)
    d.rectangle([MARGIN, 37, RIGHT, 39], fill=INK)
    centered(d, 50, "THE WORLD IN ONE DAY", font(SERIF_BOLD, 60), INK)
    centered(
        d,
        122,
        "WEDNESDAY  ·  25 NOVEMBER 2026",
        font(SANS_BOLD, 27),
        (164, 44, 44),
    )
    d.rectangle([MARGIN, 162, RIGHT, 164], fill=INK)

    # --- featured story: the Chen Jining investigation ---------------
    band_y0, band_y1 = 172, 388
    d.rectangle([MARGIN, band_y0, RIGHT, band_y1], fill=NAVY)
    d.rectangle([MARGIN, band_y0, RIGHT, band_y0 + 4], fill=GOLD)
    chip(d, MARGIN + 28, band_y0 + 24, "TOP STORY — SHANGHAI, CHINA", GOLD, font(SANS_BOLD, 20))
    head_fnt = font(SANS_BLACK, 41)
    d.text((MARGIN + 28, band_y0 + 62), "China Probes Politburo Member", font=head_fnt, fill=BAND_TEXT)
    d.text((MARGIN + 28, band_y0 + 108), "and Shanghai Chief Chen Jining", font=head_fnt, fill=BAND_TEXT)
    d.text(
        (MARGIN + 28, band_y0 + 160),
        "Shanghai's party leadership pledges loyalty to Beijing after",
        font=font(SANS, 23),
        fill=(214, 222, 235),
    )
    d.text(
        (MARGIN + 28, band_y0 + 187),
        "the anti-graft body opens a probe into its top official.",
        font=font(SANS, 23),
        fill=(214, 222, 235),
    )

    # --- story rows ---------------------------------------------------
    stories = [
        ("2", "US JURY", (179, 57, 57),
         "US Jury Convicts Huawei of Stealing Trade Secrets",
         "A federal jury finds the Chinese tech giant guilty of trade-secret theft."),
        ("3", "TECH", (56, 97, 140),
         "Nvidia's Huang Says He Is in Therapy as Shares Slide",
         "A day after returning as CEO, Jensen Huang tells staff he made 'terrible mistakes'."),
        ("4", "WHITE HOUSE", (166, 124, 0),
         "Trump Pardons the Thanksgiving Turkeys",
         "The White House pardons the holiday birds a day before Thanksgiving."),
        ("5", "COLOMBIA", (42, 127, 140),
         "Gunmen Take 25 Hostage at Supermarket",
         "Armed men seize 25 people at a supermarket in Colombia, police say."),
        ("6", "SAUDI ARABIA", (108, 74, 158),
         "Riyadh Skyscraper Hit Twice in a Week",
         "Saudi Arabia condemns a 'terrorist attack' on the PIF tower."),
        ("7", "UNITED NATIONS", (142, 69, 133),
         "Five Women Killed Every Hour by Relatives in 2025",
         "The UN counts a woman killed by a partner or relative every 12 minutes."),
    ]
    y = 404
    pitch = 94
    text_x = MARGIN + 72
    max_head_w = RIGHT - text_x
    for i, (num, tag, color, headline, summary) in enumerate(stories):
        badge(d, MARGIN + 26, y + 38, num, color)
        chip(d, text_x, y, tag, color, font(SANS_BOLD, 17))
        hf = fit(d, headline, SANS_BOLD, 30, max_head_w)
        d.text((text_x, y + 28), headline, font=hf, fill=INK)
        sf = fit(d, summary, SANS, 21, max_head_w)
        d.text((text_x, y + 62), summary, font=sf, fill=(70, 72, 84))
        if i < len(stories) - 1:
            d.line([MARGIN, y + pitch - 4, RIGHT, y + pitch - 4], fill=RULE, width=2)
        y += pitch

    # --- footer -------------------------------------------------------
    d.rectangle([MARGIN, 978, RIGHT, 980], fill=INK)
    centered(
        d,
        988,
        "Sources: Reuters · AP · SCMP · Channel NewsAsia · Japan Times · UN",
        font(SANS, 17),
        FAINT,
    )
    return img


def main():
    out = Path(__file__).resolve().parent / "entry.png"
    img = render()
    img.save(out, format="PNG")
    digest = hashlib.sha256(out.read_bytes()).hexdigest()
    print(f"wrote {out} sha256={digest}")


if __name__ == "__main__":
    main()
