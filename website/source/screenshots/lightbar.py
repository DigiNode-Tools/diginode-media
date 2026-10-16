"""Give a macOS dark-mode window capture (iTerm2) a light-mode title bar.

Usage: lightbar.py <dark.png> <light.png>

Finds the title bar (the dark grey band at the top of the window), maps its greys to light-mode greys (light bar, dark
title text), and redraws the three window buttons on the light bar. Everything else - the terminal content and the
window shadow - is left as it is. Needs Pillow.
"""
import sys

from PIL import Image, ImageDraw

BAR_DARK = 41          # dark-mode title bar grey
BAR_LIGHT = 233        # light-mode title bar grey
SEPARATOR = 212        # line between the title bar and the terminal
BUTTONS = [((255, 95, 87), (226, 70, 63)), ((254, 188, 46), (225, 161, 22)), ((40, 200, 64), (20, 174, 44))]


def is_grey(p, tol=18):
    return max(p[:3]) - min(p[:3]) <= tol


def light(v, dark=BAR_DARK):
    return max(0, min(255, round(BAR_LIGHT - (v - dark) * (BAR_LIGHT - 63) / (196 - dark))))


def main(src, out):
    im = Image.open(src).convert("RGBA")
    px = im.load()
    w, h = im.size
    cx = w // 2
    # the bar: first opaque run of dark grey down the middle
    # (the bar is #29292A or #20201F, depending on the window)
    top = next(y for y in range(h) if px[cx, y][3] == 255 and is_grey(px[cx, y]) and 24 <= px[cx, y][0] <= 52)
    dark = px[cx, top + 4][0]
    bottom = top
    while bottom + 1 < h and abs(px[cx, bottom + 1][0] - dark) <= 6 and is_grey(px[cx, bottom + 1]):
        bottom += 1
    mid = (top + bottom) // 2
    left = next(x for x in range(w) if px[x, mid][3] == 255)
    right = max(x for x in range(w) if px[x, mid][3] == 255)
    # buttons: centres of the red, yellow and green blobs
    blobs = [[], [], []]
    for y in range(top, bottom + 1):
        for x in range(left, left + 90):
            r, g, b, a = px[x, y]
            if r > 200 and g < 130 and b < 120:
                blobs[0].append((x, y))
            elif r > 200 and g > 150 and b < 110:
                blobs[1].append((x, y))
            elif g > 150 and r < 140 and b < 140:
                blobs[2].append((x, y))
    centres = []
    for pts in blobs:
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        centres.append(((min(xs) + max(xs) + 1) / 2, (min(ys) + max(ys) + 1) / 2, (max(xs) - min(xs) + 1) / 2))
    # recolour the greys of the window edge, bar and separator line
    for y in range(top - 2, bottom + 2):
        for x in range(left - 1, right + 2):
            r, g, b, a = px[x, y]
            # only the window itself: the faint shadow around the rounded corners (black, under 20% opaque) stays
            if a < 50 or not is_grey((r, g, b)):
                continue
            v = SEPARATOR if y == bottom + 1 else light((r + g + b) / 3, dark)
            px[x, y] = (v, v, v, a)
    # redraw the buttons (4x, then scaled down, so they stay smooth)
    s = 4
    for (fill, edge), (bx, by, rad) in zip(BUTTONS, centres):
        size = int(rad * 2 + 6)
        x0, y0 = int(bx - size / 2), int(by - size / 2)
        patch = Image.new("RGBA", (size * s, size * s), (0, 0, 0, 0))
        d = ImageDraw.Draw(patch)
        c = (bx - x0) * s, (by - y0) * s
        R = rad * s
        d.ellipse([c[0] - R - 1.5 * s, c[1] - R - 1.5 * s, c[0] + R + 1.5 * s, c[1] + R + 1.5 * s], fill=(BAR_LIGHT,) * 3 + (255,))
        d.ellipse([c[0] - R, c[1] - R, c[0] + R, c[1] + R], fill=edge + (255,))
        d.ellipse([c[0] - R + 0.75 * s, c[1] - R + 0.75 * s, c[0] + R - 0.75 * s, c[1] + R - 0.75 * s], fill=fill + (255,))
        patch = patch.resize((size, size), Image.LANCZOS)
        im.alpha_composite(patch, (x0, y0))
    im.save(out, optimize=True)
    print(f"{out}: bar {top}-{bottom}, window {left}-{right}, buttons {[(round(a), round(b)) for a, b, _ in centres]}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
