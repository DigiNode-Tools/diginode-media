#!/usr/bin/env python3
"""Make light and dark versions of a real iTerm window capture, keeping the true macOS window edge and shadow.

Usage: windowbar.py <capture.png> <light.png> <dark.png>

The capture must come out with a white title bar (as they do on this Mac). Only the title bar's inside is recoloured,
and the window buttons are redrawn in their normal active colours (the capture's are dimmed, or marked while a job
runs). Terminal content, edge and shadow are untouched, so both versions line up exactly. Needs Pillow.
"""
import sys

from PIL import Image, ImageDraw

LIGHT_BAR, DARK_BAR = 233, 32
TEXT_LIGHT, TEXT_DARK = 92, 150       # title text, on each bar
BUTTONS = [((255, 95, 87), (226, 70, 63)), ((254, 188, 46), (225, 161, 22)), ((40, 200, 64), (20, 174, 44))]
SCALE = 8


def bar_rows(im):
    """First and last row of the title bar's inside, down the middle of the window."""
    x = im.width // 2
    top = next(y for y in range(im.height) if im.getpixel((x, y))[3] == 255)
    end = next(y for y in range(top, im.height) if sum(im.getpixel((x, y))[:3]) == 0)
    return top, end


def button_row(im, top, end):
    """The centres and radius of the three buttons: the saturated pixels at the left of the bar."""
    xs, ys = [], []
    for y in range(top, end):
        for x in range(im.width // 3):
            r, g, b, a = im.getpixel((x, y))
            if a == 255 and max(r, g, b) - min(r, g, b) > 40:
                xs.append(x)
                ys.append(y)
    groups = []
    for x in sorted(set(xs)):
        if groups and x - groups[-1][-1] <= 1:
            groups[-1].append(x)
        else:
            groups.append([x])
    groups = [g for g in groups if len(g) >= 8][:3]
    if len(groups) < 3:  # An inactive window's buttons are grey: they are always in the same place
        return [72.0, 95.0, 118.0], 54.0, 7.0
    return [(g[0] + g[-1] + 1) / 2 for g in groups], (min(ys) + max(ys) + 1) / 2, (groups[0][-1] - groups[0][0] + 1) / 2


def recolour(im, top, end, bar, text, centres, cy, radius, source=255):
    out = im.copy()
    px = out.load()
    for y in range(top, end):
        for x in range(out.width):
            r, g, b, a = px[x, y]
            if a == 0 or (r, g, b) == (0, 0, 0):
                continue
            if max(r, g, b) - min(r, g, b) > 40 and x < out.width // 3:
                px[x, y] = (bar, bar, bar, a)  # the old button, redrawn below
                continue
            v = (r + g + b) / 3
            n = round(bar + (source - v) * (text - bar) / (source - 60))
            n = max(0, min(255, n))
            px[x, y] = (n, n, n, a)
    pad = int(radius) + 2
    for cx, (fill, edge) in zip(centres, BUTTONS):
        box = (int(cx) - pad, int(cy) - pad, int(cx) + pad + 1, int(cy) + pad + 1)
        size = (box[2] - box[0]) * SCALE, (box[3] - box[1]) * SCALE
        art = Image.new("RGBA", size, (0, 0, 0, 0))
        d = ImageDraw.Draw(art)
        ox, oy, r = (cx - box[0]) * SCALE, (cy - box[1]) * SCALE, radius * SCALE
        d.ellipse((ox - r, oy - r, ox + r, oy + r), fill=edge)
        r -= SCALE * 0.75
        d.ellipse((ox - r, oy - r, ox + r, oy + r), fill=fill)
        out.alpha_composite(art.resize((box[2] - box[0], box[3] - box[1]), Image.LANCZOS), box[:2])
    return out


def main(src, light, dark):
    im = Image.open(src).convert("RGBA")
    top, end = bar_rows(im)
    centres, cy, radius = button_row(im, top, end)
    print(f"bar rows {top}-{end - 1}, buttons at {centres}, y {cy}, radius {radius}")
    recolour(im, top, end, LIGHT_BAR, TEXT_LIGHT, centres, cy, radius).save(light, optimize=True)
    recolour(im, top, end, DARK_BAR, TEXT_DARK, centres, cy, radius).save(dark, optimize=True)


if __name__ == "__main__":
    main(*sys.argv[1:4])
