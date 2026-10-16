import json
import subprocess
import sys

H = "diginode-testnet"
CSS = "@import url(https://cdn.jsdelivr.net/npm/@fontsource/cascadia-mono@5.3.0/400.css);"
HEAD = ["Windows PowerShell", "Copyright (C) Microsoft Corporation. All rights reserved.", "",
        "Try the new cross-platform PowerShell https://aka.ms/pscore6", "",
        f"PS C:\\Users\\olly&gt; <span style='color:#f9f1a5'>ssh</span> digibyte@{H}.local"]
AUTH = [f"The authenticity of host '{H}.local (192.168.1.22)' can't be established.",
        "ECDSA key fingerprint is SHA256:RK936/oQu315J7QeH8SqR1ROqdRMWMPIaCsyI6Ivk/E.",
        "Are you sure you want to continue connecting (yes/no/[fingerprint])? yes"]
WARN = f"Warning: Permanently added '{H}.local,192.168.1.22' (ECDSA) to the list of known hosts."
PASS = f"digibyte@{H}.local's password:"
MOTD = [f"Linux {H} 6.1.21-v8+ #1642 SMP PREEMPT Mon Apr  3 17:24:16 BST 2023 aarch64", "",
        "The programs included with the Debian GNU/Linux system are free software;",
        "the exact distribution terms for each program are described in the",
        "individual files in /usr/share/doc/*/copyright.", "",
        "Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent",
        "permitted by applicable law.",
        "Last login: Sat Dec  9 13:09:36 2023 from 192.168.1.55", "",
        "Wi-Fi is currently blocked by rfkill.",
        "Use raspi-config to set the country before use.", ""]
FINAL = f"<span style='color:#13a10e'>digibyte@{H}</span>:<span style='color:#3b78ff'>~ $</span>"

jobs = {
    "Screenshot-2023-12-08-192652-1": dict(w=965, h=519, right=955, lines=HEAD),
    "Screenshot-2023-12-08-192822": dict(w=963, h=517, right=953, lines=HEAD + AUTH),
    "Screenshot-2023-12-08-192905": dict(w=967, h=519, right=957, lines=HEAD + AUTH + [WARN, PASS]),
    "Screenshot-2023-12-09-145732": dict(w=935, h=556, right=918, lines=HEAD + AUTH + [WARN, PASS] + MOTD + [FINAL], tab=f"digibyte@{H}: ~"),
}
for name, j in jobs.items():
    job = {"src": f"{name}.png", "out": f"{name}-testnet.png", "w": j["w"], "h": j["h"], "css": CSS,
           "covers": [[2, 46, j["right"] - 2, j["h"] - 46 - 6, "#0c0c0c"]],
           "blocks": [{"x": 9, "y": 51, "font": "'Cascadia Mono'", "size": 15, "lh": 19, "color": "#cccccc", "lines": j["lines"]}]}
    if j.get("tab"):
        job["covers"].append([44, 14, 172, 24, "#0c0c0c"])
        job["blocks"].append({"x": 46, "y": 17, "font": "'Segoe UI',-apple-system,sans-serif", "size": 12, "lh": 18, "color": "#ffffff", "lines": [j["tab"]]})
    json.dump(job, open(f"job-{name}.json", "w"))
    subprocess.run([sys.executable, "term.py", f"job-{name}.json"], check=True)
