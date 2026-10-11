"""Render a DigiNode Tools terminal screen as a PNG.

Replays a `script` recording (made on the DigiNode) into a terminal emulator and draws the final screen.
Usage: render-screenshot.py RECORDING COLS ROWS OUT.png [crop_top crop_bottom]
Needs: pip install pyte pillow   (uses the Menlo font, so run it on a Mac)"""
import sys
import re
import pyte
from pyte import charsets as cs
from PIL import Image, ImageDraw, ImageFont

rec, cols, rows, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
crop = (int(sys.argv[5]), int(sys.argv[6])) if len(sys.argv) > 6 else (0, rows)

screen = pyte.Screen(cols, rows)
stream = pyte.ByteStream(screen)
data = open(rec, "rb").read().decode("utf-8", "replace")

# pyte ignores the VT100 line-drawing charset in UTF-8 mode, which dialog uses for its boxes, so translate those
# sections to Unicode box characters here (leaving escape sequences untouched)
ESC_SEQ = re.compile(r"\x1b(\[[0-?]*[ -/]*[@-~]|\][^\x07]*\x07|[()][0-9A-Za-z]|.)", re.S)
buf, g0_gfx, g1_gfx, shifted, i = [], False, True, False, 0
while i < len(data):
    if data[i] == "\x1b":
        m = ESC_SEQ.match(data, i)
        seq = m.group(0) if m else data[i]
        if seq[1:2] == "(":
            g0_gfx = seq[2:] == "0"
        elif seq[1:2] == ")":
            g1_gfx = seq[2:] == "0"
        else:
            buf.append(seq)
        i += len(seq)
        continue
    c = data[i]
    if c == "\x0e":
        shifted = True
    elif c == "\x0f":
        shifted = False
    elif (g1_gfx if shifted else g0_gfx):
        buf.append(c.translate(cs.VT100_MAP))
    else:
        buf.append(c)
    i += 1
stream = pyte.Stream(screen)
stream.feed("".join(buf))

# xterm-style palette (similar to iTerm's default dark theme)
PALETTE = {
    "black": (0, 0, 0), "red": (201, 27, 0), "green": (0, 194, 0), "brown": (199, 196, 0),
    "yellow": (199, 196, 0), "blue": (2, 37, 199), "magenta": (201, 48, 199), "cyan": (0, 197, 199),
    "white": (199, 199, 199),
    "brightblack": (103, 103, 103), "brightred": (255, 110, 103), "brightgreen": (95, 250, 104),
    "brightyellow": (255, 252, 103), "brightblue": (104, 113, 255), "brightmagenta": (255, 119, 255),
    "brightcyan": (96, 253, 255), "brightwhite": (255, 255, 255),
}
DEFAULT_FG, DEFAULT_BG = (220, 220, 220), (16, 16, 20)

def colour(name, default, bold=False):
    if name == "default":
        return default
    if len(name) == 6:
        try:
            return tuple(int(name[i:i + 2], 16) for i in (0, 2, 4))
        except ValueError:
            pass
    if bold and ("bright" + name) in PALETTE:
        return PALETTE["bright" + name]
    return PALETTE.get(name, default)

SIZE = 26
font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", SIZE, index=0)
bold_font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", SIZE, index=1)
cw = round(font.getlength("M"))
ch = round(SIZE * 1.22)
pad = 24

r0, r1 = crop
img = Image.new("RGB", (cols * cw + pad * 2, (r1 - r0) * ch + pad * 2), DEFAULT_BG)
draw = ImageDraw.Draw(img)

for y in range(r0, r1):
    line = screen.buffer[y]
    for x in range(cols):
        c = line[x]
        fg = colour(c.fg, DEFAULT_FG, c.bold)
        bg = colour(c.bg, DEFAULT_BG)
        if c.reverse:
            fg, bg = bg, fg
        px, py = pad + x * cw, pad + (y - r0) * ch
        if bg != DEFAULT_BG:
            draw.rectangle([px, py, px + cw, py + ch], fill=bg)
        # Draw box lines as solid lines, so they join up (font glyphs leave gaps between rows)
        arms = {"─": "lr", "━": "lr", "│": "ud", "┃": "ud", "┌": "rd", "┐": "ld", "└": "ru", "┘": "lu",
                "├": "udr", "┤": "udl", "┬": "lrd", "┴": "lru", "┼": "lrud",
                "═": "lr", "║": "ud", "╔": "rd", "╗": "ld", "╚": "ru", "╝": "lu", "╠": "udr", "╣": "udl",
                "╦": "lrd", "╩": "lru", "╬": "lrud"}.get(c.data)
        if arms:
            cx, cy, w = px + cw // 2, py + ch // 2, 2
            double = c.data in "═║╔╗╚╝╠╣╦╩╬"
            for off in ((-3, 3) if double else (0,)):
                if "l" in arms: draw.line([px, cy + off, cx, cy + off], fill=fg, width=w)
                if "r" in arms: draw.line([cx, cy + off, px + cw, cy + off], fill=fg, width=w)
                if "u" in arms: draw.line([cx + off, py, cx + off, cy], fill=fg, width=w)
                if "d" in arms: draw.line([cx + off, cy, cx + off, py + ch], fill=fg, width=w)
            continue
        if c.data.strip():
            boxchar = "\u2500" <= c.data[0] <= "\u259f"
            draw.text((px, py + 2), c.data, font=bold_font if c.bold and not boxchar else font, fill=fg)

img.save(out)
print("saved", out, img.size)
