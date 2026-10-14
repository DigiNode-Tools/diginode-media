# DigiNode Tools media

Screenshots and images for [DigiNode Tools](https://github.com/DigiNode-Tools/diginode-tools): release notes, release announcements (Telegram and Bluesky), the website and the sponsor pages.

They live here, not in the diginode-tools repo, because every DigiNode downloads that repo when it installs or updates DigiNode Tools - images there would be downloaded to every user's DigiNode for no reason.

## Layout

- `screenshots/<feature>/` - screenshots of a feature, e.g. `screenshots/auto-updates/menu.png`. Folders are named by
  feature (not release number) so the links never change.
- `sponsor/` - images for sponsoring DigiNode Tools: `sponsor-banner.png` (leads people to diginode.tools/sponsors; used in the
  diginode-sponsors README) and `kofi-banner.png` (the Ko-fi cover, 1500x500 at 2x). `dgb-donation-qr.png` and
  `dgb-donation-card.png` are for the **original** DGB donation address only - each donation now goes to a new address, so
  the current QR code and card are drawn automatically in [diginode-sponsors](https://github.com/DigiNode-Tools/diginode-sponsors/tree/main/images).
  Don't use these two anywhere new. How they were drawn: `sponsor/source/dgb-donation-qr.md`.
- `website/` - images for the diginode.tools website, e.g. `website/tronbyt-header.png`. Sources and how to draw
  them again: `website/source/README.md`.
- `tools/render-screenshot.py` - renders a terminal screen recorded on a DigiNode as a clean PNG.

Images are added to a release note in `docs/release_notes.md` (diginode-tools repo) with an image line under the note,
using the raw URL. The text in square brackets is the alt text (a description for people who can't see the image):

```
- New: DigiNode Setup can now install operating system updates for you automatically...
  ![The new Automatic System Updates menu in DigiNode Setup](https://raw.githubusercontent.com/DigiNode-Tools/diginode-media/main/screenshots/auto-updates/menu.png)
```

The image then appears under that note in the GitHub release, on that note's post in the Bluesky thread, and in a
photo album after the Telegram announcement. Usually at most one image per note, and only for things you can see.

## Making a screenshot

1. On the DigiNode, set a tidy terminal size and record the screen:
   ```
   stty cols 100 rows 30
   script -q -f -c "diginode-setup" ~/cap.txt
   ```
2. Go to the screen you want, then (while it is showing) copy the recording to your Mac:
   ```
   scp diginode:cap.txt .
   ```
3. Render it (the last screen in the recording is drawn):
   ```
   python3 tools/render-screenshot.py cap.txt 100 30 screenshot.png
   ```

## Licence

The logo and screenshots can be used to link to or write about DigiNode Tools without asking - see [LICENCE.md](LICENCE.md) and the [name and logo policy](https://github.com/DigiNode-Tools/diginode-tools/blob/main/TRADEMARKS.md). The DigiNode Tools logo includes the DigiByte logo (MIT, [DigiByte-Core/digibyte-logos](https://github.com/DigiByte-Core/digibyte-logos)).
