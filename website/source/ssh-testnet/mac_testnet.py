import html
import json
import subprocess
import sys

COLS = 84
H = "diginode-testnet"
PROMPT = "<span style='color:#8cf77b'>➜</span>  <span style='color:#5ff0f0'>~</span> ssh digibyte@%s.local" % H
CUR = "<span style='background:#e6e6e6'> </span>"


def wrap(lines):
    out = []
    for l in lines:
        if l.startswith("<"):
            out.append(l)
            continue
        while len(l) > COLS:
            out.append(html.escape(l[:COLS]))
            l = l[COLS:]
        out.append(html.escape(l))
    return out


AUTH = [f"The authenticity of host '{H}.local (192.168.1.22)' can't be established.",
        "ED25519 key fingerprint is SHA256:/rZl/6EU/eRNolfkEGXtuSdrd2NBKKhAGIncToJ7t84.",
        "This host key is known by the following other names/addresses:",
        "    ~/.ssh/known_hosts:31: 192.168.1.22",
        "Are you sure you want to continue connecting (yes/no/[fingerprint])? yes"]
WARN = f"Warning: Permanently added '{H}.local' (ED25519) to the list of known hosts."
PASS = f"digibyte@{H}.local's password: "
MOTD = [f"Linux {H} 5.15.61-v8+ #1579 SMP PREEMPT Fri Aug 26 11:16:44 BST 2022 aarch64", "",
        "The programs included with the Debian GNU/Linux system are free software;",
        "the exact distribution terms for each program are described in the",
        "individual files in /usr/share/doc/*/copyright.", "",
        "Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent",
        "permitted by applicable law.",
        "Last login: Mon Jan  9 17:53:41 2023 from 192.168.1.78", "",
        "Wi-Fi is currently blocked by rfkill.",
        "Use raspi-config to set the country before use.", ""]
FINAL = (f"<span style='color:#8cf77b;font-weight:700'>digibyte@{H}</span>:<span style='color:#6f8cff;font-weight:700'>~ $</span> " + CUR)


def title(text):
    return {"x": 150, "y": 41, "w": 410, "h": 20, "bg": "#fafafa", "text": text, "font": "-apple-system,'SF Pro Text',sans-serif",
            "size": 13, "color": "#4c4c4c", "weight": 600}


def block(lines):
    return {"x": 61, "y": 69, "font": "Menlo", "size": 11.65, "lh": 15, "color": "#e6e6e6", "lines": lines}


jobs = {
    "image-82": dict(h=475, bottom=398, lines=[PROMPT, CUR], title=f"ssh digibyte@{H}.local"),
    "image-83": dict(h=460, bottom=383, lines=[PROMPT] + wrap(AUTH)[:-1] + [wrap(AUTH)[-1] + CUR], title=f"ssh digibyte@{H}.local"),
    "image-84": dict(h=460, bottom=383, lines=[PROMPT] + wrap(AUTH + [WARN]) + [html.escape(PASS) + "<span class='key'></span>"], title=f"ssh digibyte@{H}.local"),
    "image-85": dict(h=475, bottom=398, lines=[PROMPT] + wrap(AUTH + [WARN, PASS.rstrip()] + MOTD) + [FINAL], title=f"digibyte@{H}: ~"),
}
for name, j in jobs.items():
    job = {"src": f"{name}.png", "out": f"{name}-testnet.png", "w": 710, "h": j["h"],
           # the key icon iTerm shows at a password prompt, copied from the original screenshot
           "css": ".key{display:inline-block;width:9px;height:15px;vertical-align:top;background:url(data:image/png;base64,%s) -310px -%dpx}" % (
               __import__("base64").b64encode(open("image-84.png", "rb").read()).decode(), 69 + 15 * 7),
           "covers": [[58, 68, 594, j["bottom"] - 68, "#000"]],
           "titles": [title(j["title"])],
           # a full terminal scrolls: keep only the lines that fit
           "blocks": [block(j["lines"][-((j["bottom"] - 69) // 15):])]}
    json.dump(job, open(f"job-{name}.json", "w"))
    subprocess.run([sys.executable, "term.py", f"job-{name}.json"], check=True)
