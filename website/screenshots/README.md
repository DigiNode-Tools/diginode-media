# DigiNode Tools screenshots for the website (2026-10-16)

Captured on Olly's Raspberry Pi (DigiNode Tools develop = v26.10.05, DigiByte Core v9.26.7) in iTerm2, as macOS
window captures WITH the window shadow (`screencapture -l<window id>`, window in front).

- **DigiNode Setup screens** (`diginode-setup-*.png`, `diginode-motd.png`): terminal **80 columns x 28 rows** -> 682x569.
  Keep this size for every new Setup screenshot so they all have the same shape (the main menu, 23x74, is the
  tallest dialog). Since v26.10.05 every Setup dialog fits 80 columns.
- Screens that don't fit (`diginode-help.png`) are captured at **100x35** (same shape) and scaled to 682x569.
- Menu screens that would change settings even when you back out (Chain, Tor, UPnP, System...) were drawn on the
  Pi with the exact `dialog` command from diginode-setup.sh - nothing was changed.
- **DigiNode Dashboard** (`diginode-dashboard.png`): 100x53 with N pressed (IP addresses hidden). Edited: the
  "DIGIASSET NODE" sponsor row was removed and "dev-branch" replaced with v26.10.05 (the line was printed by the
  same terminal and copied in). Recapture after a release if the Dashboard changes.
