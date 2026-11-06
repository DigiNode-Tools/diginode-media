#!/usr/bin/env python3
#
# Name:    tourframes.py
# Purpose: Frames for the home page's menu tour, in the same window for light and dark mode. Every Setup screen gets
#          the same title bar (so nothing flickers between frames), taken from the main menu captures. New captures
#          only exist with a light bar, so their dark versions get the dark capture's bar.
#
# Usage:   tourframes.py <output folder>     (writes <folder>/light/*.png and <folder>/dark/*.png; needs Pillow)

import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import windowbar  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.normpath(os.path.join(HERE, "..", "..", "screenshots"))
SETUP = ["diginode-setup-main-menu", "diginode-setup-wallets", "diginode-setup-update", "diginode-setup-system-updates", "diginode-setup-chain", "diginode-setup-tor"]
OTHER = []


def bar_end():
    """The last row of the title bar: where the light and dark main menu captures stop differing a lot."""
    light = Image.open(os.path.join(SHOTS, "diginode-setup-main-menu.png")).convert("RGB")
    dark = Image.open(os.path.join(SHOTS, "dark", "diginode-setup-main-menu.png")).convert("RGB")
    x = light.width // 2
    rows = [y for y in range(120) if abs(light.getpixel((x, y))[0] - dark.getpixel((x, y))[0]) > 60]
    return rows[-1] + 1


def darken(im, end):
    """The same window with a dark title bar: only the bar's inside changes, and the buttons are redrawn."""
    top, _ = windowbar.bar_rows(im)
    centres, cy, radius = windowbar.button_row(im, top, end)
    return windowbar.recolour(im, top, end, windowbar.DARK_BAR, windowbar.TEXT_DARK, centres, cy, radius, source=233)


def main():
    out = sys.argv[1]
    end = bar_end()
    bars = {
        "light": Image.open(os.path.join(SHOTS, "diginode-setup-main-menu.png")).convert("RGBA").crop((0, 0, 682, end)),
        "dark": Image.open(os.path.join(SHOTS, "dark", "diginode-setup-main-menu.png")).convert("RGBA").crop((0, 0, 682, end)),
    }
    for mode, bar in bars.items():
        os.makedirs(os.path.join(out, mode), exist_ok=True)
        for name in SETUP:
            im = Image.open(os.path.join(SHOTS, name + ".png")).convert("RGBA")  # newest terminal content
            # Every frame gets the main menu's title bar, then the dark version is that same window recoloured, so the
            # window's edge and shadow are the true ones (a pasted dark capture left a black edge and a step in the shadow)
            im.paste(bars["light"], (0, 0))
            if mode == "dark":
                im = darken(im, end)
            im.save(os.path.join(out, mode, name + ".png"), optimize=True)
        for name in OTHER:
            src = os.path.join(SHOTS, "dark", name + ".png") if mode == "dark" else os.path.join(SHOTS, name + ".png")
            Image.open(src).save(os.path.join(out, mode, name + ".png"), optimize=True)
    print(f"title bar: rows 0-{end - 1}")


if __name__ == "__main__":
    main()
