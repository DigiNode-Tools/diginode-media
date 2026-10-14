# The DGB donation QR code

`../dgb-donation-qr.png`: the DigiNode Tools donation address as a dotted QR code, with the DigiNode logo in the middle
(error correction H, so the logo doesn't stop it scanning). To draw it again (e.g. for a new address):

```bash
swift matrix.swift dgb1qv8psxjeqkau5s35qwh75zy6kp95yhxxw0d3kup > matrix.txt   # the QR code's modules, from macOS
python3 styled_qr.py matrix.txt diginode-logo-round.png dgb-donation-qr.html   # prints the size, e.g. 1230
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --hide-scrollbars \
  --window-size=1230,1230 --screenshot=../dgb-donation-qr.png dgb-donation-qr.html
```

Then draw `../dgb-donation-card.png` again (the command is at the top of `dgb-donation-card.html`), and check both
scan before publishing. Everything links to the images here, so they update everywhere - except Ko-fi, which keeps
its own copy (upload the new card to the pinned post there).
