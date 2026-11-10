"""Icône de l'app FM-1 Émulateur : l'esprit Guru~600 (panneau noir, joues en bois, onde rouge LED, nom crème)."""
import math, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

UNC = os.path.expanduser("~/Documents/FM-1/p600/fonts/American Uncial MN.otf")
N = 1024
BG, CREAM, RED = (14, 13, 12), (238, 232, 216), (255, 64, 48)


def icon():
    im = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    mask = Image.new("L", (N, N), 0)
    ImageDraw.Draw(mask).rounded_rectangle((100, 100, 924, 924), 185, fill=255)   # gabarit macOS (824 px, marges)
    body = Image.new("RGBA", (N, N), BG + (255,))
    d = ImageDraw.Draw(body)
    for y in range(100, 924):                       # léger dégradé du panneau
        v = int(10 + 14 * (1 - (y - 100) / 824))
        d.line((100, y, 924, y), fill=(v + 4, v + 3, v + 2, 255))
    for x0 in (100, 864):                           # les joues en bois du Prophet
        for x in range(x0, x0 + 60):
            for y in range(100, 924, 1):
                g = 0.5 + 0.5 * math.sin(y / 9.0 + math.sin(y / 53.0) * 3 + x / 31.0)
                c = (int(96 + 40 * g), int(52 + 22 * g), int(26 + 10 * g), 255)
                body.putpixel((x, y), c)
    # l'onde rouge LED (dents de scie) avec un halo
    glow = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    pts, x = [], 180
    while x < 844:
        pts += [(x, 360), (x, 300), (x + 166, 360)]
        x += 166
    gd.line(pts, fill=RED + (255,), width=14, joint="curve")
    halo = glow.filter(ImageFilter.GaussianBlur(18))
    body = Image.alpha_composite(body, halo)
    body = Image.alpha_composite(body, glow)
    d = ImageDraw.Draw(body)
    f1 = ImageFont.truetype(UNC, 205)
    d.text((512, 560), "Guru", font=f1, fill=CREAM, anchor="mm")
    f2 = ImageFont.truetype(UNC, 140)
    d.text((512, 760), "~600", font=f2, fill=RED, anchor="mm")
    im.paste(body, (0, 0), mask)
    return im


def main(out_dir):
    im = icon()
    im.save(os.path.join(out_dir, "icone_1024.png"))
    iconset = os.path.join(out_dir, "Guru600.iconset")
    os.makedirs(iconset, exist_ok=True)
    for s in (16, 32, 128, 256, 512):
        im.resize((s, s), Image.LANCZOS).save(os.path.join(iconset, f"icon_{s}x{s}.png"))
        im.resize((2 * s, 2 * s), Image.LANCZOS).save(os.path.join(iconset, f"icon_{s}x{s}@2x.png"))
    subprocess.run(["iconutil", "-c", "icns", iconset, "-o", os.path.join(out_dir, "Guru600.icns")], check=True)
    print("ok")


if __name__ == "__main__":
    main(sys.argv[1])
