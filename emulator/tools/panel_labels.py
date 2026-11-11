#!/usr/bin/env python3
"""Guru-600: the FM-1 panel's printed words on its buttons and keys, as alpha masks for panel.rs.

The FM-1 prints its button words (FX, SEL… HOME, PLAY/STOP, OCT-/OCT+) in a wide bold face and
its key words (OP1…POLY) in a plain sans; the silkscreen above the knobs is a dot font (panel.rs
draws that one itself). This renders each word once per panel scale (1: the browser's panel,
2: the native window's) into crates/fm1-live/src/panel_labels.bin:
    for each word: scale (u8), length (u8), the word, width (u16 LE), height (u16 LE), w*h alpha bytes
Sizes are the official photos' (cuvave.com, the FM-1's front view, 1000 px), scaled as panel.rs draws them.

    python3 tools/panel_labels.py [BUTTON_FONT] [KEY_FONT]
"""
import os, struct, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "crates/fm1-live/src/panel_labels.bin")
BUTTON_FONT = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/Library/Fonts/Virage-WideBold.otf")
KEY_FONT = sys.argv[2] if len(sys.argv) > 2 else "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
K1 = 240 / 153         # panel pixels per photo pixel at scale 1 for the keys (panel.rs K1)
KC = K1                # ... for the buttons (the same: panel.rs draws all but the screen at K1)
# (words, font, cap height and the width of a reference word in photo pixels, panel pixels per photo pixel)
SETS = [
    (["FX", "SEL", "ENV", "LFO", "EDIT", "GLO", "HOME", "SAVE", "ARP", "SEQ", "PLAY", "STOP", "REC", "OCT-", "OCT+"],
     BUTTON_FONT, 8.1, ("HOME", 32.5), KC),
    (["OP1", "OP2", "OP3", "OP4", "OP5", "OP6", "PIT", "GLO.", "MONO", "POLY"], KEY_FONT, 6.8, ("OP1", 16.2), K1),
]
SS = 8  # supersampling


def render(word, font_path, cap, ref, k, scale):
    text = word.rstrip(".")  # GLO. : the key's GLO, in the key font
    big = 200
    f = ImageFont.truetype(font_path, big)
    capb = f.getbbox("H")
    cap_px = capb[3] - capb[1]
    refb = f.getbbox(ref[0])
    # target sizes in panel pixels
    th = cap * k * scale
    sy = th / cap_px
    sx = (ref[1] * k * scale) / ((refb[2] - refb[0]) * sy) * sy
    b = f.getbbox(text)
    w, h = b[2] - b[0] + 20, big + 40
    im = Image.new("L", (w, h), 0)
    ImageDraw.Draw(im).text((10 - b[0], 20), text, font=f, fill=255)
    # a band around the capitals, as much above as below (Q's tail fits): centring the mask
    # centres the capitals
    top, pad = 20 + capb[1], round(cap_px * 0.3)
    im = im.crop((0, top - pad, w, top + cap_px + pad))
    bb = im.getbbox()
    im = im.crop((bb[0], 0, bb[2], im.height))
    ow = max(1, round(im.width * sx))
    oh = max(1, round(im.height * sy))
    oh += oh % 2 != round(th) % 2   # (the band's middle on the capitals' middle)
    return im.resize((ow, oh), Image.LANCZOS)


def main():
    out = bytearray()
    for scale in (1, 2):
        for words, font, cap, ref, k in SETS:
            for word in words:
                im = render(word, font, cap, ref, k, scale)
                name = word.encode()
                out += struct.pack("<BB", scale, len(name)) + name + struct.pack("<HH", im.width, im.height) + im.tobytes()
    open(OUT, "wb").write(out)
    print(f"{OUT}: {len(out)} bytes")


if __name__ == "__main__":
    main()
