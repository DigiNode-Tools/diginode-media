#!/usr/bin/env python3
#
# Name:    build.py
# Purpose: Draw the social share cards for diginode.tools (1200x630 - Open Graph / X / Bluesky / Telegram previews) from
#          cards.json, with headless Chrome. Output: ../../share/<id>.png (diginode-media/website/share/).
#          Each card: the page's section, title and subtitle, its address, and a picture - an image from assets/ (as a
#          cut-out or in a screenshot frame), or hand-made artwork from art/<name>.html (icons from assets/*.svg).
#
# Usage:   website/source/share-cards/build.py [id ...]     (no ids = all cards)

import base64
import html
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "share"))
FONTS = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Nunito+Sans:ital,wght@0,600;0,700;0,800;1,800'
         '&display=block">')


def data_uri(name):
    ext = name.rsplit(".", 1)[-1].replace("jpg", "jpeg")
    with open(os.path.join(HERE, "assets", name), "rb") as f:
        return f"data:image/{ext};base64," + base64.b64encode(f.read()).decode()


def chrome():
    for c in (os.environ.get("CHROME"), "google-chrome", "chromium", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"):
        if c and (shutil.which(c) or os.path.exists(c)):
            return shutil.which(c) or c
    sys.exit("Google Chrome not found")


def svg_icon(name, color, size):
    """An icon from assets/<name>.svg (Simple Icons, CC0), recoloured; or a full-colour SVG if color is 'original'."""
    with open(os.path.join(HERE, "assets", name + ".svg"), encoding="utf-8") as f:
        svg = f.read()
    if color != "original":
        svg = svg.replace("<svg ", f'<svg fill="{color}" ', 1)
    return svg.replace("<svg ", f'<svg width="{size}" height="{size}" ', 1)


def art_html(name):
    """A hand-made picture from art/<name>.html. {{icon:NAME:COLOR:SIZE}} inserts an icon."""
    import re
    with open(os.path.join(HERE, "art", name + ".html"), encoding="utf-8") as f:
        s = f.read()
    s = re.sub(r"\{\{icon:([a-z0-9-]+):([^:}]+):(\d+)\}\}", lambda m: svg_icon(m[1], m[2], m[3]), s)
    return re.sub(r"\{\{img:([^}]+)\}\}", lambda m: data_uri(m[1]), s)


def step_html(step, os_name):
    """Raspberry Pi guide steps: the step number in a ring, the Raspberry Pi logo, progress through steps 1-7, and
    the computer it's for (Mac / Windows) if any."""
    main = int("".join(ch for ch in step if ch.isdigit()))
    dots = "".join(f'<i class="{"on" if n == main else "done" if n < main else ""}">{n}</i>' for n in range(1, 8))
    for_os = f'<div class="os">For {html.escape(os_name)}</div>' if os_name else ""
    return f'''<style>
.step{{position:absolute;right:70px;top:70px;width:460px;display:flex;flex-direction:column;align-items:center;gap:24px}}
.step .ring{{width:250px;height:250px;border-radius:50%;background:#0066CC;display:flex;flex-direction:column;align-items:center;justify-content:center;
  box-shadow:0 0 0 14px rgba(90,169,255,.14),0 0 0 30px rgba(90,169,255,.06),0 0 80px rgba(90,169,255,.45)}}
.step .ring small{{font-weight:800;font-size:26px;letter-spacing:4px;color:#cfe4ff}}
.step .ring b{{font-weight:800;font-style:italic;font-size:118px;line-height:.95}}
.step .dots{{display:flex;gap:10px;margin-top:14px}}
.step .dots i{{width:44px;height:44px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-style:normal;font-weight:800;font-size:20px;
  border:2px solid rgba(156,200,255,.35);color:#9cc8ff}}
.step .dots i.done{{background:rgba(0,102,204,.45);color:#fff;border-color:transparent}}
.step .dots i.on{{background:#fff;color:#002352;border-color:#fff}}
.step .os{{font-weight:800;font-size:24px;padding:8px 22px;border-radius:999px;background:rgba(255,255,255,.1);border:2px solid rgba(156,200,255,.3)}}
.step .rp{{position:absolute;right:-6px;top:-20px}}
</style>
<div class="step"><span class="rp">{svg_icon("raspberrypi", "#C51A4A", 56)}</span>
  <div class="ring"><small>STEP</small><b>{html.escape(step)}</b></div>
  <div class="dots">{dots}</div>{for_os}</div>'''


def card_html(c):
    e = html.escape
    pic = c.get("image", {})
    if pic.get("style") == "step":
        picture = step_html(pic["step"], pic.get("os", ""))
    elif pic.get("style") == "art":
        picture = art_html(pic["file"])
    elif pic.get("style") == "screenshot":
        picture = (f'<div class="shot" style="{pic.get("css", "")}"><div class="bar"><i></i><i></i><i></i></div>'
                   f'<img src="{data_uri(pic["file"])}"></div>')
    elif pic:
        picture = f'<img class="cutout" src="{data_uri(pic["file"])}" style="{pic.get("css", "")}">'
    else:
        picture = f'<img class="badge" src="{data_uri("diginode-logo-round.png")}">'
    return f'''<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1200px;height:630px;overflow:hidden}}
body{{font-family:"Nunito Sans",sans-serif;color:#fff;position:relative;
  background:radial-gradient(ellipse at 18% 20%,#0b3a7a 0%,#002352 55%,#001631 100%)}}
body::before{{content:"";position:absolute;inset:0;opacity:.18;
  background-image:radial-gradient(#5aa9ff 1.2px,transparent 1.3px);background-size:26px 26px}}
.text{{position:absolute;left:72px;top:64px;width:{c.get("text_width", 600)}px;display:flex;flex-direction:column;gap:18px}}
.logo{{width:{c.get("logo_width", 230)}px;opacity:.95}}
.eyebrow{{margin-top:22px;font-weight:800;font-size:22px;letter-spacing:3px;text-transform:uppercase;color:#7fb8ff}}
h1{{font-weight:800;font-style:italic;font-size:{c.get("title_size", 64)}px;line-height:1.04;letter-spacing:-1.5px;text-wrap:balance}}
p{{font-weight:600;font-size:27px;line-height:1.35;color:#cfe4ff;text-wrap:pretty}}
.url{{position:absolute;left:72px;bottom:54px;font-weight:800;font-size:26px;letter-spacing:.3px;
  background:#0066CC;border-radius:999px;padding:10px 28px;box-shadow:0 6px 18px rgba(0,0,0,.35)}}
.cutout{{position:absolute;filter:drop-shadow(0 18px 30px rgba(0,0,0,.45))}}
.badge{{position:absolute;right:90px;top:155px;width:320px;height:320px;border-radius:50%;
  box-shadow:0 0 0 14px rgba(90,169,255,.12),0 0 0 30px rgba(90,169,255,.06),0 0 90px rgba(90,169,255,.45)}}
.shot{{position:absolute;border-radius:14px;overflow:hidden;background:#0d1117;box-shadow:0 20px 50px rgba(0,0,0,.55);
  border:1px solid rgba(156,200,255,.25)}}
.shot .bar{{height:30px;background:#e8e8ea;display:flex;gap:8px;align-items:center;padding:0 12px}}
.shot .bar i{{width:12px;height:12px;border-radius:50%;background:#ff5f57}}
.shot .bar i:nth-child(2){{background:#febc2e}} .shot .bar i:nth-child(3){{background:#28c840}}
.shot img{{display:block;width:100%}}
</style></head><body>
{picture}
<div class="text">
  <img class="logo" src="{data_uri("logo-white.png")}">
  {f'<div class="eyebrow">{e(c["eyebrow"])}</div>' if c.get("eyebrow") else ''}
  <h1>{e(c["title"])}</h1>
  {f'<p>{e(c["subtitle"])}</p>' if c.get("subtitle") else ''}
</div>
<div class="url">{e(c["url"])}</div>
</body></html>'''


def main():
    with open(os.path.join(HERE, "cards.json"), encoding="utf-8") as f:
        cards = json.load(f)["cards"]
    want = set(sys.argv[1:])
    os.makedirs(OUT, exist_ok=True)
    for c in cards:
        if want and c["id"] not in want:
            continue
        with tempfile.TemporaryDirectory() as tmp:
            page = os.path.join(tmp, "card.html")
            with open(page, "w", encoding="utf-8") as f:
                f.write(card_html(c))
            out = os.path.join(OUT, c["id"] + ".png")
            subprocess.run([chrome(), "--headless", "--hide-scrollbars", "--disable-gpu", "--virtual-time-budget=15000",
                            "--window-size=1200,630", f"--screenshot={out}", "file://" + page], check=True, capture_output=True)
        print("drew", c["id"])


if __name__ == "__main__":
    main()
