#!/usr/bin/env python3
# Draw a dotted QR code (round dots, round finder patterns, DigiNode badge in the middle) as an HTML page with an SVG,
# from a module grid (one line of 0/1 per row, as printed by matrix.swift).
# Usage: styled_qr.py MATRIX.txt LOGO.png OUT.html
import base64, sys

rows = [l.strip() for l in open(sys.argv[1]) if l.strip()]
# Crop the generator's quiet zone
top = next(i for i, r in enumerate(rows) if "1" in r)
bottom = max(i for i, r in enumerate(rows) if "1" in r)
left = min(r.index("1") for r in rows if "1" in r)
right = max(r.rindex("1") for r in rows if "1" in r)
grid = [r[left:right + 1] for r in rows[top:bottom + 1]]
n = len(grid)

M = 30                 # px per module
QUIET = 2              # modules of white around the code
size = (n + 2 * QUIET) * M
logo = base64.b64encode(open(sys.argv[2], "rb").read()).decode()

def finder(x, y):
    return x < 7 and y < 7 or x >= n - 7 and y < 7 or x < 7 and y >= n - 7

BADGE = 11             # badge diameter in modules (about 9% of the code's area - fine with error correction H)
c = n / 2
def in_badge(x, y):
    return (x + 0.5 - c) ** 2 + (y + 0.5 - c) ** 2 <= (BADGE / 2 + 0.6) ** 2

out = []
for y in range(n):
    for x in range(n):
        if grid[y][x] == "1" and not finder(x, y) and not in_badge(x, y):
            out.append(f'<circle cx="{(x + QUIET + .5) * M}" cy="{(y + QUIET + .5) * M}" r="{M * .43:.1f}"/>')
for fx, fy in [(0, 0), (n - 7, 0), (0, n - 7)]:
    cx, cy = (fx + QUIET + 3.5) * M, (fy + QUIET + 3.5) * M
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{3 * M}" fill="none" stroke="#000" stroke-width="{M}"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{1.5 * M}"/>')

cx = cy = size / 2
R = BADGE / 2 * M                  # badge radius
ring = R * 0.30                    # width of the blue ring
tr = R - ring / 2                  # radius the ring text runs along
inner = R - ring                   # logo radius
font = ring * 0.52
badge = f'''
<circle cx="{cx}" cy="{cy}" r="{R}" fill="#0066CC"/>
<defs>
 <path id="top" d="M {cx - tr} {cy} A {tr} {tr} 0 0 1 {cx + tr} {cy}"/>
 <path id="bottom" d="M {cx - tr} {cy} A {tr} {tr} 0 0 0 {cx + tr} {cy}"/>
 <clipPath id="clip"><circle cx="{cx}" cy="{cy}" r="{inner}"/></clipPath>
</defs>
<g fill="#fff" font-family="Avenir Next, Helvetica Neue, Arial, sans-serif" font-weight="800" font-size="{font:.1f}" letter-spacing="2">
 <text dominant-baseline="central"><textPath href="#top" startOffset="50%" text-anchor="middle">DIGINODE TOOLS</textPath></text>
 <text dominant-baseline="central"><textPath href="#bottom" startOffset="50%" text-anchor="middle">DONATE DGB</textPath></text>
</g>
<image href="data:image/png;base64,{logo}" x="{cx - inner}" y="{cy - inner}" width="{2 * inner}" height="{2 * inner}" clip-path="url(#clip)"/>
'''

print(f'''<!doctype html><html><head><meta charset="utf-8"><style>*{{margin:0}}html,body{{width:{size}px;height:{size}px;overflow:hidden;background:#fff}}</style></head><body>
<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">
<rect width="{size}" height="{size}" fill="#fff"/>
<g fill="#000">{"".join(out)}</g>{badge}</svg></body></html>''', file=open(sys.argv[3], "w"))
print(size)
