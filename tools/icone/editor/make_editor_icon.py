"""Icône de l'application Guru-600 Editor (16/11/2026, Marc) : l'icône Guru-600 (icone_1024.png), « guru 600 » un peu
réduit et remonté, « EDITOR » dessous (fonte Guru600), sur un fond d'une autre teinte (rotation de teinte), pour la
distinguer des autres icônes.   make_editor_icon.py [teinte en degrés] [sortie.png]"""
import colorsys, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

H = os.path.dirname(os.path.abspath(__file__)); P = os.path.dirname(H)
SRC = os.path.join(P, "icone_1024.png"); FONT = os.path.join(P, "..", "fonts", "guru600", "Guru600.ttf")


def hue_rotate(a, deg):
    rgb = a[..., :3] / 255.0
    mx, mn = rgb.max(-1), rgb.min(-1); d = mx - mn
    hh = np.zeros_like(mx)
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    m = d > 1e-6
    i = m & (mx == r); hh[i] = ((g - b)[i] / d[i]) % 6
    i = m & (mx == g); hh[i] = (b - r)[i] / d[i] + 2
    i = m & (mx == b); hh[i] = (r - g)[i] / d[i] + 4
    hh = (hh / 6 + deg / 360.0) % 1.0
    s = np.where(mx > 0, d / np.maximum(mx, 1e-6), 0); v = mx
    i6 = np.floor(hh * 6).astype(int) % 6; f = hh * 6 - np.floor(hh * 6)
    p, q, t = v * (1 - s), v * (1 - s * f), v * (1 - s * (1 - f))
    out = np.stack([np.choose(i6, [v, q, p, p, t, v]), np.choose(i6, [t, v, v, q, p, p]), np.choose(i6, [p, p, t, v, v, q])], -1)
    a = a.copy(); a[..., :3] = np.clip(out * 255, 0, 255); return a


def main(deg=150.0, out=os.path.join(H, "icone_editor_1024.png")):
    import cv2
    src = np.array(Image.open(SRC).convert("RGBA"))
    Y0, Y1, X0, X1 = 560, 862, 190, 834                            # « guru 600 » (mesuré : 575-848)
    lum = src[..., :3].max(-1).astype(int)
    m = np.zeros(lum.shape, np.uint8); m[Y0:Y1, X0:X1] = (lum[Y0:Y1, X0:X1] > 70).astype(np.uint8) * 255
    m = cv2.dilate(m, np.ones((23, 23), np.uint8))
    # le fond sans le texte (inpainting), puis toute l'icône dans l'autre teinte
    clean = src.copy()
    clean[..., :3] = cv2.cvtColor(cv2.inpaint(cv2.cvtColor(src[..., :3], cv2.COLOR_RGB2BGR), m, 9, cv2.INPAINT_TELEA), cv2.COLOR_BGR2RGB)
    # (what the effacement left at its edges, brighter than the panel around: effaced too)
    cl = clean[..., :3].max(-1).astype(int); r2 = np.zeros(cl.shape, np.uint8)
    r2[Y0:Y1, X0:X1] = (cl[Y0:Y1, X0:X1] > 45).astype(np.uint8) * 255
    r2 = cv2.dilate(r2, np.ones((9, 9), np.uint8))
    clean[..., :3] = cv2.cvtColor(cv2.inpaint(cv2.cvtColor(clean[..., :3], cv2.COLOR_RGB2BGR), r2, 9, cv2.INPAINT_TELEA), cv2.COLOR_BGR2RGB)
    base = hue_rotate(clean.astype(float), deg).astype(np.uint8)
    # le texte : ce qui se détache du fond effacé ; le crème garde sa couleur, le contour (saturé) prend la teinte
    diff = np.abs(src[..., :3].astype(int) - clean[..., :3].astype(int)).max(-1)
    a = np.clip((diff - 12) / 45.0, 0, 1); a[:Y0] = 0; a[Y1:] = 0; a[:, :X0] = 0; a[:, X1:] = 0
    a = a * (m > 0); a = cv2.GaussianBlur(a, (0, 0), 0.8)   # (only around the letters: no specks)
    rgb = src[..., :3].astype(float) / 255; sat = (rgb.max(-1) - rgb.min(-1)) / np.maximum(rgb.max(-1), 1e-6)
    rotsrc = hue_rotate(src.astype(float), deg)[..., :3]
    w8 = np.clip((sat - 0.25) / 0.2, 0, 1)[..., None]
    col = (src[..., :3] * (1 - w8) + rotsrc * w8).astype(np.uint8)
    txt = np.dstack([col, (a * 255).astype(np.uint8)])[Y0:Y1, X0:X1]
    t = Image.fromarray(txt, "RGBA"); k = 0.76; w, h = int(t.width * k), int(t.height * k)
    t = t.resize((w, h), Image.LANCZOS)
    b = Image.fromarray(base, "RGBA"); top = 548
    b.alpha_composite(t, ((1024 - w) // 2, top))
    d = ImageDraw.Draw(b); f = ImageFont.truetype(FONT, 78); y = top + h + 52
    sh = Image.new("RGBA", b.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).text((512, y), "EDITOR", font=f, fill=(0, 0, 0, 200), anchor="mm", stroke_width=6, stroke_fill=(0, 0, 0, 200))
    b.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
    d.text((512, y), "EDITOR", font=f, fill=(246, 241, 222, 255), anchor="mm", stroke_width=2, stroke_fill=(246, 241, 222, 255))
    b.save(out); print(out)


if __name__ == "__main__":
    main(float(sys.argv[1]) if len(sys.argv) > 1 else 150.0, *(sys.argv[2:3] or []))
