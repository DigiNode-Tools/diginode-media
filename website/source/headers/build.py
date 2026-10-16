#!/usr/bin/env python3
#
# Name:    build.py
# Purpose: Draw the header pictures for diginode.tools pages - transparent 1000x333 artwork (drawn at 3x, 3000x999) that
#          floats over the titlebar's blockchain background, like Raspberry-Pi-DigiNode.png. Each header is
#          headers/<id>.html; {{icon:NAME:COLOR:SIZE}} and {{img:FILE}} come from ../share-cards/assets/ (same as the
#          share cards' art). Output: ../../headers/<id>.png (diginode-media/website/headers/).
#          With --preview, also draws ../../headers/preview/<id>.png: the header on the real titlebar background with
#          the page title, so it can be checked before it goes on the website.
#
# Usage:   website/source/headers/build.py [--preview] [id ...]     (no ids = all headers)

import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "share-cards"))
import build as cards  # noqa: E402  (svg_icon, data_uri, chrome)

OUT = os.path.normpath(os.path.join(HERE, "..", "..", "headers"))
FONTS = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Nunito+Sans:ital,wght@0,600;0,700;0,800;1,800'
         '&family=Roboto:wght@300&family=JetBrains+Mono:wght@600&display=block">')
# The titlebar on diginode.tools: blockchain.jpg under a navy layer (rgb 13,31,67 at 70%), title in Roboto Light 36px
BACKGROUND = os.path.join(HERE, "blockchain.jpg")
TITLES = {
    "sponsors": "Sponsors",
    "port-tester": "DigiByte Port Tester",
    "advanced-features": "Advanced Features",
    "why-run": "Unlocking the Power of Decentralization: Why You Should Run a DigiNode",
    "additional-features": "Additional Features",
    "release-notes": "Release Notes",
    "system-requirements": "System Requirements",
    "licence": "Software Licence",
    "faq": "Frequently Asked Questions",
    "support": "Support",
}


def header_html(name):
    with open(os.path.join(HERE, name + ".html"), encoding="utf-8") as f:
        s = f.read()
    s = re.sub(r"\{\{icon:([a-z0-9-]+):([^:}]+):(\d+)\}\}", lambda m: cards.svg_icon(m[1], m[2], m[3]), s)
    s = re.sub(r"\{\{img:([^}]+)\}\}", lambda m: cards.data_uri(m[1]), s)
    return f'''<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1000px;height:333px;background:transparent;overflow:hidden}}
body{{font-family:"Nunito Sans",sans-serif;color:#fff;position:relative}}
</style></head><body>{s}</body></html>'''


def shoot(html_text, out, size, scale=1, transparent=False):
    with tempfile.TemporaryDirectory() as tmp:
        page = os.path.join(tmp, "page.html")
        with open(page, "w", encoding="utf-8") as f:
            f.write(html_text)
        args = [cards.chrome(), "--headless", "--hide-scrollbars", "--disable-gpu", "--virtual-time-budget=15000",
                f"--window-size={size}", f"--force-device-scale-factor={scale}", f"--screenshot={out}"]
        if transparent:
            args.append("--default-background-color=00000000")
        subprocess.run(args + ["file://" + page], check=True, capture_output=True)


def preview_html(png, title):
    return f'''<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>
*{{margin:0;padding:0}}
body{{width:1400px;height:458px;overflow:hidden;position:relative;background:url("file://{BACKGROUND}") center/cover}}
body::before{{content:"";position:absolute;inset:0;background:rgba(13,31,67,.7)}}
img{{position:absolute;left:200px;top:30px;width:1000px;height:333px}}
h1{{position:absolute;left:0;right:0;top:363px;text-align:center;font:300 36px Roboto,Arial,sans-serif;color:#fff}}
</style></head><body><img src="file://{png}"><h1>{title}</h1></body></html>'''


def main():
    args = sys.argv[1:]
    preview = "--preview" in args
    want = [a for a in args if a != "--preview"]
    ids = want or sorted(f[:-5] for f in os.listdir(HERE) if f.endswith(".html"))
    os.makedirs(os.path.join(OUT, "preview"), exist_ok=True)
    for i in ids:
        png = os.path.join(OUT, i + ".png")
        shoot(header_html(i), png, "1000,333", scale=3, transparent=True)
        print("drew", i)
        if preview:
            shoot(preview_html(png, TITLES.get(i, i)), os.path.join(OUT, "preview", i + ".png"), "1400,458")


if __name__ == "__main__":
    main()
