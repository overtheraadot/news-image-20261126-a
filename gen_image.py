#!/usr/bin/env python3
"""Draw the 26 November 2026 world-news front page (1024x1024 PNG).

Fresh code written for news-image-20261126, account A (overtheraa).
Stories were researched from live news reports of Thursday 26 Nov 2026.
Deterministic: same bytes on every run (no timestamps, no randomness).
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

NAVY = (16, 32, 64)
PAPER = (247, 243, 234)
INK = (24, 24, 24)
OCEAN = (207, 227, 238)
LAND = (46, 93, 67)
LAND_EDGE = (28, 66, 46)
RED = (178, 34, 34)
GOLD = (212, 175, 55)

# (tag, region colour, headline)
STORIES = [
    ("MIDDLE EAST", (178, 34, 34), "Houthis hit Saudi Ras Tanura refinery; Brent tops $94"),
    ("N. AMERICA", (16, 32, 64), "Macy's 100th parade moved to Saturday as storm hits NYC"),
    ("S. ASIA", (146, 90, 0), "India marks Constitution Day and 18 years since 26/11"),
    ("MARKETS", (0, 96, 96), "Nasdaq slides nearly 4% as AI fears rout US stocks"),
    ("MIDDLE EAST", (178, 34, 34), "Two oil tankers strike mines in the Strait of Hormuz"),
    ("N. AMERICA", (16, 32, 64), "Thanksgiving Day: Trump proclaims a national day of thanks"),
    ("EUROPE", (64, 64, 160), "EU leaders meet in Brussels over the 2028-34 budget"),
    ("S. ASIA", (146, 90, 0), "Gukesh faces Sindarov in the World Chess Championship"),
    ("AFRICA", (120, 70, 140), "Kenya discharges last Ebola patient; DRC toll tops 5,300"),
    ("E. ASIA", (0, 110, 60), "US plans tariffs on 14 partners; Taiwan faces up to 15%"),
    ("S. ASIA", (146, 90, 0), "Sooryavanshi, 15, smashes 204 off 53 balls vs UAE"),
    ("MIDDLE EAST", (178, 34, 34), "Israel strikes Hamas official in Gaza; truce under strain"),
    ("EUROPE", (64, 64, 160), "Norway top court voids disputed oil licences"),
    ("AFRICA", (120, 70, 140), "Ghana unveils Heritage Series banknotes"),
    ("E. ASIA", (0, 110, 60), "Taiwan shares plunge 1,927 points as dollar weakens"),
    ("S. ASIA", (146, 90, 0), "IPL 2027 auction draws a record 1,220 players"),
    ("N. AMERICA", (16, 32, 64), "US Army calls Iowa explosives blast a 'huge success'"),
    ("AFRICA", (120, 70, 140), "Protest outside S. African court as migrant rallies barred"),
    ("MIDDLE EAST", (178, 34, 34), "Israeli judges urge dropping bribery case against Netanyahu"),
    ("S. ASIA", (146, 90, 0), "Flipkart chief Krishnamurthy to step down in December"),
    ("LATIN AM.", (150, 60, 90), "Colombia police free 20 hostages after 17-hour siege"),
    ("EUROPE", (64, 64, 160), "Russia's own data: nearly 500,000 war dead in Ukraine"),
    ("AFRICA", (120, 70, 140), "Kenya wins 293,600 jobs in Saudi Arabia"),
    ("S. ASIA", (146, 90, 0), "India gives Nepal a Rs 15,000-crore aid package"),
    ("E. ASIA", (0, 110, 60), "North Korea expels Swiss diplomat in sanctions row"),
    ("S. ASIA", (146, 90, 0), "IITs to add 6,000 seats in robotics, AI and space"),
    ("N. AMERICA", (16, 32, 64), "Fort Hood survivors lose final appeal on execution witness"),
    ("AFRICA", (120, 70, 140), "DRC president signs constitutional reform law"),
    ("MIDDLE EAST", (178, 34, 34), "Cairo tanker fire kills at least 30, injures 19"),
    ("S. ASIA", (146, 90, 0), "Hasina asks to return to Bangladesh on 16 December"),
    ("LATIN AM.", (150, 60, 90), "Mexico's Sheinbaum vows sweeping gambling reform"),
    ("EUROPE", (64, 64, 160), "Hera probe sends close-ups of asteroid crater"),
    ("AFRICA", (120, 70, 140), "Sao Tome reappoints PM Americo Ramos"),
    ("S. ASIA", (146, 90, 0), "Bangladesh garment workers win a 36% pay rise"),
    ("SE ASIA", (0, 120, 120), "Indonesia sets 11 Dec vote to fill vice presidency"),
    ("N. AMERICA", (16, 32, 64), "Search under way for six after plane crashes in Gulf of Mexico"),
    ("AFRICA", (120, 70, 140), "Nigeria starts building its own naval ships"),
    ("S. ASIA", (146, 90, 0), "First Pakistani astronaut joins China's Shenzhou-24"),
    ("LATIN AM.", (150, 60, 90), "Brazil betting tax haul hits R$12bn through October"),
    ("OCEANIA", (40, 110, 140), "Australia apologises to LGBTQ veterans for past injustices"),
]

# Rough continent outlines as (lon, lat) points, equirectangular projection.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 74), (-75, 72),
     (-60, 60), (-55, 47), (-65, 45), (-75, 35), (-80, 26), (-85, 20), (-90, 15),
     (-95, 16), (-105, 20), (-115, 25), (-125, 40), (-140, 60), (-165, 60)],
    [(-55, 60), (-45, 60), (-40, 70), (-55, 76), (-65, 75)],
    [(-80, 10), (-70, 12), (-60, 8), (-50, 0), (-35, -8), (-40, -20), (-50, -30),
     (-60, -35), (-70, -45), (-73, -55), (-70, -30), (-75, -18), (-80, -5)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31), (35, 28), (43, 12),
     (51, 11), (48, 0), (40, -10), (35, -20), (30, -30), (20, -35), (15, -27),
     (12, -18), (9, 0), (9, 4), (-8, 5), (-15, 12)],
    [(-10, 36), (0, 44), (-2, 48), (5, 55), (10, 57), (18, 56), (21, 60), (25, 65),
     (30, 70), (40, 68), (55, 70), (70, 73), (90, 75), (110, 76), (130, 72), (150, 70),
     (170, 67), (178, 65), (170, 60), (160, 55), (150, 50), (140, 40), (130, 35),
     (127, 40), (120, 30), (110, 20), (105, 10), (100, 8), (95, 15), (90, 22), (80, 10),
     (75, 8), (70, 20), (60, 25), (55, 27), (50, 30), (45, 29), (40, 36), (35, 36),
     (30, 36), (25, 40), (20, 40), (15, 44), (10, 44), (3, 43), (-2, 37), (-9, 37)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (130, -32), (137, -35), (140, -38),
     (145, -38), (150, -37), (153, -27), (150, -22), (146, -19), (142, -11), (137, -12),
     (132, -12), (126, -14), (122, -17), (118, -20)],
    [(-4, 50), (-1, 51), (1, 52), (0, 54), (-3, 56), (-5, 58), (-5, 53), (-3, 50)],
    [(130, 31), (133, 34), (137, 35), (140, 38), (141, 42), (143, 44), (141, 45),
     (140, 40), (136, 35), (132, 33)],
    [(95, 16), (98, 14), (100, 8), (104, 2), (108, -2), (112, -7), (115, -8), (118, -9),
     (120, -10), (114, -10), (108, -7), (103, -2), (99, 5), (96, 10)],
    [(122, 18), (124, 16), (122, 13), (120, 14), (121, 18)],
]

# (lon, lat, label) for story dots on the map.
DOTS = [
    (50, 26, ""), (55, 24, ""), (35, 32, ""), (34, 31, ""), (31, 30, ""),
    (-74, 41, ""), (-95, 30, ""), (-90, 30, ""), (-100, 38, ""), (-122, 37, ""),
    (10, 51, ""), (10, 60, ""), (37, 56, ""), (77, 28, ""), (72, 20, ""),
    (90, 24, ""), (100, 14, ""), (121, 25, ""), (127, 40, ""), (139, 35, ""),
    (18, -34, ""), (36, -1, ""), (8, 6, ""), (28, -2, ""), (47, 15, ""),
    (-74, 5, ""), (-100, 19, ""), (-52, -10, ""), (133, -25, ""), (67, 30, ""),
]

REGION_LABELS = [
    (-125, 62, "NORTH AMERICA"), (-62, -18, "SOUTH AMERICA"),
    (12, 68, "EUROPE"), (17, 8, "AFRICA"), (42, 46, "MIDEAST"),
    (88, 46, "S. ASIA"), (115, 52, "EAST ASIA"), (108, -12, "S.E. ASIA"),
    (135, -38, "OCEANIA"),
]


def project(lon, lat, x0, y0, x1, y1):
    x = x0 + (lon + 170.0) / 360.0 * (x1 - x0)
    y = y0 + (75.0 - lat) / 130.0 * (y1 - y0)
    return (x, y)


def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- header band ---
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.rectangle([0, 148, W, 152], fill=GOLD)
    f_date = ImageFont.truetype(FONTB, 52)
    d.text((32, 22), "THURSDAY 26 NOVEMBER 2026", font=f_date, fill=(255, 255, 255))
    f_sub = ImageFont.truetype(FONTB, 21)
    d.text((32, 92), "THE WORLD IN ONE DAY  \u2022  40 STORIES  \u2022  9 REGIONS",
           font=f_sub, fill=GOLD)
    f_tag = ImageFont.truetype(FONTB, 15)
    d.text((32, 122), "WORLD NEWS  \u2014  EVERY STORY FIRST REPORTED ON THIS DAY",
           font=f_tag, fill=(180, 200, 225))

    # --- world map strip ---
    mx0, my0, mx1, my1 = 24, 168, 1000, 330
    d.rectangle([mx0, my0, mx1, my1], fill=OCEAN, outline=NAVY, width=2)
    for poly in CONTINENTS:
        pts = [project(lon, lat, mx0, my0, mx1, my1) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_EDGE)
    for lon, lat, _ in DOTS:
        x, y = project(lon, lat, mx0, my0, mx1, my1)
        d.ellipse([x - 3.5, y - 3.5, x + 3.5, y + 3.5], fill=RED, outline=(255, 255, 255))
    f_map = ImageFont.truetype(FONTB, 12)
    for lon, lat, label in REGION_LABELS:
        x, y = project(lon, lat, mx0, my0, mx1, my1)
        tw = d.textlength(label, font=f_map)
        lx, ly = x - tw / 2, y - 7
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            d.text((lx + dx, ly + dy), label, font=f_map, fill=(255, 255, 255))
        d.text((lx, ly), label, font=f_map, fill=NAVY)

    # --- story grid: 4 columns x 10 rows ---
    f_tag2 = ImageFont.truetype(FONTB, 10)
    f_head = ImageFont.truetype(FONTB, 12)
    gx0, gy0 = 24, 348
    cw, ch = 242, 64
    for i, (tag, colour, head) in enumerate(STORIES):
        col, row = i % 4, i // 4
        x = gx0 + col * (cw + 4)
        y = gy0 + row * ch
        d.rectangle([x, y, x + cw - 2, y + ch - 6], fill=(255, 255, 255),
                    outline=(200, 196, 186), width=1)
        d.rectangle([x, y, x + 4, y + ch - 6], fill=colour)
        d.text((x + 12, y + 5), tag, font=f_tag2, fill=colour)
        lines = wrap(d, head, f_head, cw - 24)[:3]
        ly = y + 19
        for line in lines:
            d.text((x + 12, ly), line, font=f_head, fill=INK)
            ly += 14

    # --- footer ---
    d.line([24, 992, 1000, 992], fill=NAVY, width=2)
    f_foot = ImageFont.truetype(FONT, 13)
    d.text((24, 1000), "All 40 stories were first reported on Thursday 26 November 2026.",
           font=f_foot, fill=INK)
    f_foot2 = ImageFont.truetype(FONTB, 13)
    d.text((700, 1000), "make.fun  \u2022  news-image-20261126", font=f_foot2, fill=NAVY)

    img.save("entry.png", format="PNG")
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
