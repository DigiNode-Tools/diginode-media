"""Animated 'drag Raspberry Pi Imager to Applications' for the guide's step 2 (macOS), from a capture of the installer
window. Usage: draggif.py <window.png> <icon.png> <out.gif>"""
import os
import subprocess
import sys
import tempfile

win, icon, out = sys.argv[1:4]
SIZE = 138                     # icon PNG size so the visible icon matches the window's (~110px)
START = (152, 232)             # centre of the app icon in the window
END = (450, 232)               # centre of the Applications folder
CURSOR = "M0,0 L0,17 L4,13 L7,20 L10,19 L7,12 L12,12 Z"   # macOS-style arrow


def run(*a):
    subprocess.run(["magick", *a], check=True)


tmp = os.path.join(os.path.dirname(os.path.abspath(out)), "dragframes"); os.makedirs(tmp, exist_ok=True)
if True:
    ghost = os.path.join(tmp, "ghost.png")
    run(icon, "-resize", f"{SIZE}x{SIZE}", "-channel", "A", "-evaluate", "multiply", "0.6", "+channel", ghost)
    frames, delays = [], []

    def frame(pos, highlight=False, cursor=True, ghosted=True, delay=4):
        f = os.path.join(tmp, f"f{len(frames):03d}.png")
        args = [win]
        if highlight:   # Finder darkens the drop target
            args += ["-fill", "rgba(0,0,0,0.10)", "-draw", f"roundrectangle {END[0]-70},{END[1]-70} {END[0]+70},{END[1]+70} 10,10"]
        if ghosted and pos:
            args += [ghost, "-geometry", f"+{int(pos[0]-SIZE/2)}+{int(pos[1]-SIZE/2)}", "-composite"]
        if cursor and pos:
            cx, cy = int(pos[0] + 8), int(pos[1] + 12)
            args += ["-stroke", "white", "-strokewidth", "1.5", "-fill", "black",
                     "-draw", f"translate {cx},{cy} path '{CURSOR}'"]
        run(*args, f)
        frames.append(f)
        delays.append(delay)

    # 1. Still, the cursor resting on the app icon
    frame(START, ghosted=False, delay=100)
    # 2. Drag across (eased)
    steps = 22
    for i in range(1, steps + 1):
        t = i / steps
        e = t * t * (3 - 2 * t)
        x = START[0] + (END[0] - START[0]) * e
        y = START[1] - 30 * (4 * t * (1 - t)) + (END[1] - START[1]) * e   # a slight arc
        frame((x, y), highlight=t > 0.8)
    # 3. Over the folder, then drop
    frame(END, highlight=True, delay=60)
    frame(None, cursor=False, ghosted=False, delay=200)
    args = []
    for f, d in zip(frames, delays):
        args += ["-delay", str(d), f]
    run(*args, "-loop", "0", "-quality", "90", "-define", "webp:lossless=false", out)
print("drew", out, len(frames), "frames")
