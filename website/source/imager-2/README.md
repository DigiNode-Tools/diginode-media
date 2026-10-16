# Raspberry Pi Imager 2 screenshots (guide steps 2 and 3)

`../../guide/imager-2/` - Raspberry Pi Imager v2.0.12, captured on macOS on 2026-10-16 while Olly clicked through it
with the guide's settings (Raspberry Pi 5, Raspberry Pi OS Lite (64-bit), hostname `diginode`, user `digibyte`, SSH
with a password).

- `imager2-mac-*.png`: the macOS window (window capture, no shadow).
- `imager2-win-*.png`: the same screens with a Windows 11 title bar instead (`winframe.py`) - the app looks the
  same inside on both.
- The Storage and summary screens showed Olly's backup drive, so the drive was redrawn as a USB NVMe dock
  ("Realtek RTL9210B-CG Media", 1 TB) and "Wi-Fi configured" removed (`j-storage.json`, `j-summary.json`, drawn with
  `../ssh-testnet/term.py`). The ERASE warning (`12-erase`) is drawn (`j-erase.json`) - nothing was written.
- `imager2-mac-install-drag.webp`: dragging Imager to Applications, made from the installer window and the app's
  icon (`draggif.py`).

Replace with new captures when Imager's look changes.

- `imager2-download-mac.png` / `-win.png`: raspberrypi.com/software (captured from a browser window on 2026-10-16, cropped, download link highlighted).
