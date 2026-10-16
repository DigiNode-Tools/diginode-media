# Raspberry Pi Imager 2 screenshots (guide steps 2 and 3)

`../../guide/imager-2/` - Raspberry Pi Imager v2.0.12, captured on macOS on 2026-10-16 while Olly clicked through it
with the guide's settings (Raspberry Pi 5, Raspberry Pi OS Lite (64-bit), hostname `diginode`, user `digibyte`, SSH
with a password).

- `imager2-mac-*.png`: the macOS window (window capture, no shadow).
- `imager2-win-*.png`: the same screens with a Windows 11 title bar instead (`winframe.py`), then recoloured to
  Imager's Windows red (#8C393C instead of the Mac's #AB1E3A) with the real Windows title-bar icon
  (`windows/recolour.sh`, 2026-10-16 - checked against the real app in a Windows 11 VM). Layout is the same on both.
- The Storage and summary screens showed Olly's backup drive, so the drive was redrawn as a USB NVMe dock
  ("Realtek RTL9210B-CG Media", 1 TB) and "Wi-Fi configured" removed (`j-storage.json`, `j-summary.json`, drawn with
  `../ssh-testnet/term.py`). The ERASE warning (`12-erase`) is drawn (`j-erase.json`) - nothing was written.
- `imager2-mac-install-drag.webp`: dragging Imager to Applications, made from the installer window and the app's
  icon (`draggif.py`).

Replace with new captures when Imager's look changes.

- `imager2-download-mac.png` / `-win.png`: raspberrypi.com/software (captured from a browser window on 2026-10-16, cropped, download link highlighted).

- `imager2-win-install-*.png` (2026-10-16): installing Imager on Windows 11 (UTM VM, Edge, 1280x800, captured from
  the Mac with `screencapture -l<window id> -o`): 01 Edge's downloads panel, 02 the permission prompt (User Account
  Control - DRAWN from `windows/uac.html`, as the VM didn't show it; publisher and name from the file's Digital
  Signatures / Details: "Raspberry Pi Limited", "Raspberry Pi Imager Setup"), 03 language, 04 welcome, 05 licence,
  06 folder, 07 desktop shortcut, 08 installing, 09 finish - all real. Cropped with red outlines (#E0102F) by
  `windows/wincrops.sh`. Imager 2's installer is Inno Setup (it was NSIS in Imager 1.x).
- `imager2-download-win.png` was replaced with a real Windows capture (Edge) the same day.
