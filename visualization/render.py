#!/usr/bin/env python3
"""Render three exact Boolean lattice diamonds and their cancellation."""
from functools import lru_cache
from math import cos, pi, sin
from os import environ
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SIZE = (636, 416)
BACKGROUND = "#0a1525"
CARD = "#12263d"
INK = "#eff7ff"
SUBTLE = "#b9cde0"
EDGE = "#567491"
INSIDE = "#68e3b9"
OUTSIDE = "#ffad7f"
CANCEL = "#fae093"
P = {1, 5, 7, 9, 25, 44, 45, 47, 61}
ROWS = ((7, 25, 31, 1), (31, 44, 63, 12), (12, 1, 13, 0))


@lru_cache
def font(size, bold=False):
    key = "Q335_BOLD_FONT" if bold else "Q335_FONT"
    name = "Arial Bold.ttf" if bold else "Arial.ttf"
    default = Path("/System/Library/Fonts/Supplemental") / name
    return ImageFont.truetype(environ.get(key, str(default)), size)


def label(draw, xy, words, size, color=INK, bold=False, anchor=None):
    draw.text(xy, words, fill=color, font=font(size, bold), anchor=anchor)


def base():
    image = Image.new("RGB", SIZE, BACKGROUND)
    draw = ImageDraw.Draw(image)
    label(draw, (20, 12), "Three inequalities, one obstruction", 30, bold=True)
    label(draw, (20, 54), "Each number encodes a set by its six membership bits.", 21, SUBTLE)
    draw.rounded_rectangle((18, 91, 618, 310), 18, fill=CARD)
    return image, draw


def diamond(phase, angle):
    image, draw = base()
    a, b, join, meet = ROWS[phase]
    label(draw, (36, 105), f"Inequality {phase + 1} of 3", 21, CANCEL, bold=True)

    def project(x, y, z):
        u = x*cos(angle) + y*sin(angle)
        depth = -x*sin(angle) + y*cos(angle)
        return 322 + 104*u, 210 - 71*z - 26*depth

    points = [project(*q) for q in ((1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1))]
    draw.polygon([points[i] for i in (2, 0, 3, 1)], fill="#183650")
    for u, v in ((2, 0), (2, 1), (0, 3), (1, 3)):
        draw.line((points[u], points[v]), fill=EDGE, width=3)
    for i, (x, y) in enumerate(points):
        mask = (a, b, join, meet)[i]
        color = INSIDE if mask in P else OUTSIDE
        if mask in (1, 12, 31):
            draw.ellipse((x-22, y-22, x+22, y+22), outline=CANCEL, width=2)
        draw.ellipse((x-17, y-17, x+17, y+17), fill=color)
        label(draw, (x, y), str(mask), 19, BACKGROUND, True, "mm")
    label(draw, (474, 133), f"Join = {join}", 22)
    label(draw, (474, 188), f"Inputs = {a}, {b}", 20)
    label(draw, (474, 245), f"Meet = {meet}", 22)
    label(draw, (20, 327), f"f({join}) + f({meet}) <= f({a}) + f({b})", 27, bold=True)
    label(draw, (20, 374), "In family", 20, INSIDE, True)
    label(draw, (160, 374), "Outside", 20, OUTSIDE, True)
    label(draw, (300, 374), "Cancels in the sum", 20, CANCEL, True)
    return image


def sum_frame():
    image, draw = base()
    label(draw, (36, 106), "Add the three inequalities", 23, CANCEL, True)
    label(draw, (36, 153), "Cancel f(1), f(12), and f(31).", 22, SUBTLE)
    label(draw, (36, 204), "f(0) + f(13) + f(63)", 24, OUTSIDE, True)
    label(draw, (292, 204), "<=", 24, INK, True)
    label(draw, (342, 204), "f(7) + f(25) + f(44)", 24, INSIDE, True)
    label(draw, (36, 247), "Outside: sum at least 3k", 19, OUTSIDE)
    label(draw, (342, 247), "Inside: sum less than 3k", 19, INSIDE)
    label(draw, (20, 329), "A strict threshold k would reverse this inequality.", 23, bold=True)
    label(draw, (20, 374), "The resulting contradiction excludes every submodular f.", 20, SUBTLE)
    return image


if __name__ == "__main__":
    frames = [diamond(stage, .35 + j*pi/11) for stage in range(3) for j in range(16)]
    frames.append(sum_frame())
    palette = Image.new("RGB", (636*4, 416))
    for i, sample in enumerate((frames[0], frames[16], frames[32], frames[-1])):
        palette.paste(sample, (636*i, 0))
    palette = palette.quantize(colors=96)
    frames = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
    output = Path(__file__).with_name("three-uncrossings.gif")
    frames[0].save(output, save_all=True, append_images=frames[1:], duration=[125]*48 + [3300],
                   loop=0, optimize=True)
