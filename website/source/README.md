# Website images

`../tronbyt-header.png` (3000x999, transparent): the header picture on the diginode.tools "DigiByte Apps for Tronbyt"
page, used in the Ark theme's "Tronbyt Titlebar" (over the same network background as the "Pi -> DigiNode Titlebar").
Two Tidbyt-style LED displays showing the DigiFacts and DigiByte Price apps.

Drawn from `tronbyt-header.html` (it uses `digifacts-frame-000.png` and `p.png`, the first frames of the apps'
screenshots) with:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --hide-scrollbars --force-device-scale-factor=3 \
  --default-background-color=00000000 --window-size=1000,333 --screenshot=../tronbyt-header.png tronbyt-header.html
```
