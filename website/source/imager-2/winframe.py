"""Turn a macOS Raspberry Pi Imager screenshot into a Windows 11 one: keep the app's content, replace the title bar.
Usage: winframe.py <mac.png> <out.png>   (mac.png: 680x482 window capture without shadow, 28px title bar)"""
import base64
import os
import subprocess
import sys
import tempfile

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
TITLE_H = 28          # macOS title bar in the capture
WIN_BAR = 32          # Windows 11 title bar
src, out = sys.argv[1], sys.argv[2]
w, h = 680, 482
b64 = base64.b64encode(open(src, "rb").read()).decode()
logo = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "..", "..", "Users", "ollystedall",
                         "Projects", "DigiNode Tools", "diginode-media", "website", "source", "share-cards", "assets", "raspberrypi.svg")).read() \
    if False else open("/Users/ollystedall/Projects/DigiNode Tools/diginode-media/website/source/share-cards/assets/raspberrypi.svg").read()
logo = logo.replace("<svg ", '<svg width="16" height="16" fill="#c51a4a" ', 1)
H = h - TITLE_H + WIN_BAR
btn = "display:flex;align-items:center;justify-content:center;width:46px;height:32px;color:#1b1b1b"
html = f"""<!doctype html><html><head><meta charset="utf-8"><style>*{{margin:0;padding:0}}
html,body{{width:{w}px;height:{H}px;overflow:hidden;background:transparent}}
.win{{position:absolute;inset:0;border:1px solid #c7c7c7;border-radius:8px;overflow:hidden;background:#fff}}
.bar{{position:absolute;left:0;right:0;top:0;height:{WIN_BAR}px;background:#f3f3f3;display:flex;align-items:center}}
.bar .t{{display:flex;align-items:center;gap:10px;padding-left:12px;font:400 12px 'Segoe UI',-apple-system,sans-serif;color:#1b1b1b;flex:1}}
.c{{position:absolute;left:-1px;top:{WIN_BAR - TITLE_H - 1}px;width:{w}px;height:{h}px;background:url(data:image/png;base64,{b64}) 0 0 no-repeat;
  clip-path:inset({TITLE_H}px 0 0 0)}}
</style></head><body><div class="win"><div class="c"></div><div class="bar"><div class="t">{logo}<span>Raspberry Pi Imager v2.0.12</span></div>
<div style="{btn}"><svg width="10" height="10"><path d="M0 5.5h10" stroke="#1b1b1b"/></svg></div>
<div style="{btn}"><svg width="10" height="10"><rect x=".5" y=".5" width="9" height="9" rx="1.5" fill="none" stroke="#1b1b1b"/></svg></div>
<div style="{btn}"><svg width="10" height="10"><path d="M.5.5l9 9M9.5.5l-9 9" stroke="#1b1b1b"/></svg></div></div></div></body></html>"""
with tempfile.TemporaryDirectory() as tmp:
    page = os.path.join(tmp, "w.html")
    open(page, "w").write(html)
    subprocess.run([CHROME, "--headless", "--hide-scrollbars", "--disable-gpu", f"--window-size={w},{H}", "--force-device-scale-factor=1",
                    "--default-background-color=00000000", f"--screenshot={out}", "file://" + page], check=True, capture_output=True)
print("drew", out)
