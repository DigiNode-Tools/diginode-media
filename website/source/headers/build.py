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

import html
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
    "rpi-setup": "Raspberry Pi Setup Guide - One Page Setup",
    "build-a-diginode": "Build a DigiNode with Raspberry Pi 4",
}


# Raspberry Pi setup guide steps: id => (step, computer, what it's about). Drawn by step_html, not from a .html file.
STEPS = {
    "rpi-step-1": ("1", "", "Assemble the case"),
    "rpi-step-2-mac": ("2", "Mac", "Install Raspberry Pi Imager"),
    "rpi-step-2-windows": ("2", "Windows", "Install Raspberry Pi Imager"),
    "rpi-step-3": ("3", "", "Write Raspberry Pi OS"),
    "rpi-step-4": ("4", "", "Connect the SSD and boot"),
    "rpi-step-5-mac": ("5", "Mac", "Connect with SSH"),
    "rpi-step-5-windows": ("5", "Windows", "Connect with SSH"),
    "rpi-step-5b-mac": ("5b", "Mac", "Find your Pi's IP address"),
    "rpi-step-5b-windows": ("5b", "Windows", "Find your Pi's IP address"),
    "rpi-step-6": ("6", "", "Run DigiNode Setup"),
    "rpi-step-7": ("7", "", "Port forwarding"),
}


def step_html(step, computer, label):
    """The guide as a journey: the Raspberry Pi board on the left, the finished DigiNode on the right, and steps 1-7
    between them. The DigiNode starts faded and grey, and becomes more solid with each step - finished at step 7."""
    main = int("".join(ch for ch in step if ch.isdigit()))
    done = (main - 1) / 6
    dots = "".join(f'<i class="{"on" if n == main else "done" if n < main else ""}">{n}</i>' for n in range(1, 8))
    for_os = f'<span class="os">For {html.escape(computer)}</span>' if computer else ""
    return f'''<style>
.board{{position:absolute;left:0;top:60px;width:300px;filter:drop-shadow(0 14px 22px rgba(0,0,0,.45))}}
.case{{position:absolute;right:0;top:44px;width:300px;opacity:{0.35 + 0.65 * done:.2f};filter:grayscale({1 - done:.2f}) drop-shadow(0 14px 22px rgba(0,0,0,.45))}}
.mid{{position:absolute;left:300px;right:300px;top:0;height:333px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px}}
.ring{{width:150px;height:150px;border-radius:50%;background:#0066CC;display:flex;flex-direction:column;align-items:center;justify-content:center;
  box-shadow:0 0 0 10px rgba(90,169,255,.15),0 0 0 22px rgba(90,169,255,.06),0 0 60px rgba(90,169,255,.45)}}
.ring small{{font-weight:800;font-size:17px;letter-spacing:3px;color:#cfe4ff}}
.ring b{{font-weight:800;font-style:italic;font-size:70px;line-height:.95}}
.label{{font-weight:800;font-size:22px;text-align:center;white-space:nowrap}}
.track{{position:relative;display:flex;gap:10px}}
.track::before{{content:"";position:absolute;left:12px;right:12px;top:50%;height:3px;margin-top:-1.5px;background:rgba(156,200,255,.25)}}
.track i{{position:relative;width:30px;height:30px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-style:normal;
  font-weight:800;font-size:14px;background:#0d1f43;border:2px solid rgba(156,200,255,.4);color:#9cc8ff}}
.track i.done{{background:#0066CC;border-color:#0066CC;color:#fff}}
.track i.on{{background:#fff;border-color:#fff;color:#002352;transform:scale(1.2)}}
.os{{white-space:nowrap;font-weight:800;font-size:16px;padding:4px 14px;margin-top:-4px;border-radius:999px;background:rgba(255,255,255,.1);border:2px solid rgba(156,200,255,.3)}}
.row{{display:flex;align-items:center;gap:12px}}
</style>
<img class="board" src="{{{{img:raspberry-pi-board.png}}}}">
<img class="case" src="{{{{img:diginode-case-cutout.png}}}}">
<div class="mid">
  <div class="ring"><small>STEP</small><b>{html.escape(step)}</b></div>
  <div class="label">{html.escape(label)}</div>
  <div class="track">{dots}</div>{for_os}
</div>'''


def step_title(name):
    step, computer, _ = STEPS.get(name, (name, "", ""))
    return f"Raspberry Pi Setup Guide - Step {step}" + (f" ({computer})" if computer else "")


def header_html(name):
    if name in STEPS:
        s = step_html(*STEPS[name])
    else:
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
    ids = want or sorted(f[:-5] for f in os.listdir(HERE) if f.endswith(".html")) + list(STEPS)
    os.makedirs(os.path.join(OUT, "preview"), exist_ok=True)
    for i in ids:
        png = os.path.join(OUT, i + ".png")
        shoot(header_html(i), png, "1000,333", scale=3, transparent=True)
        print("drew", i)
        if preview:
            shoot(preview_html(png, TITLES.get(i) or step_title(i)), os.path.join(OUT, "preview", i + ".png"), "1400,458")


if __name__ == "__main__":
    main()
