"""Redraw the text of a terminal screenshot (keeping the window) with headless Chrome.
Usage: term.py <job.json>   job: {src, out, w, h, covers:[[x,y,w,h,color]], blocks:[{x,y,font,size,lh,color,lines:[html...]}], titles:[{x,y,w,h,bg,text,font,size,color,weight}]}"""
import base64
import json
import os
import subprocess
import sys
import tempfile

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
job = json.load(open(sys.argv[1]))
src = base64.b64encode(open(job["src"], "rb").read()).decode()
parts = [f'<img src="data:image/png;base64,{src}" style="position:absolute;left:0;top:0">']
for x, y, w, h, c in job.get("covers", []):
    parts.append(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{c}"></div>')
for t in job.get("titles", []):
    parts.append(f'<div style="position:absolute;left:{t["x"]}px;top:{t["y"]}px;width:{t["w"]}px;height:{t["h"]}px;background:{t["bg"]};'
                 f'display:flex;align-items:center;justify-content:center;font:{t.get("weight", 600)} {t["size"]}px {t["font"]};color:{t["color"]}">{t["text"]}</div>')
for b in job.get("blocks", []):
    lines = "".join(f'<div style="height:{b["lh"]}px;white-space:pre">{l}</div>' for l in b["lines"])
    parts.append(f'<div style="position:absolute;left:{b["x"]}px;top:{b["y"]}px;font:{b.get("weight", 400)} {b["size"]}px {b["font"]};'
                 f'line-height:{b["lh"]}px;color:{b["color"]};-webkit-font-smoothing:antialiased">{lines}</div>')
html = (f'<!doctype html><html><head><meta charset="utf-8"><style>{job.get("css", "")}*{{margin:0;padding:0}}html,body{{width:{job["w"]}px;height:{job["h"]}px;overflow:hidden;background:transparent}}</style></head>'
        f'<body>{"".join(parts)}</body></html>')
with tempfile.TemporaryDirectory() as tmp:
    page = os.path.join(tmp, "t.html")
    open(page, "w").write(html)
    subprocess.run([CHROME, "--headless", "--hide-scrollbars", "--disable-gpu", "--virtual-time-budget=10000", f"--window-size={job['w']},{job['h']}",
                    "--force-device-scale-factor=1", "--default-background-color=00000000", f"--screenshot={job['out']}", "file://" + page],
                   check=True, capture_output=True)
print("drew", job["out"])
