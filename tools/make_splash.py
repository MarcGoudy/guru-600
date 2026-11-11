"""Écran d'accueil « Guru~600 » du firmware (240 x 240) : aperçu PNG + en-tête C (alpha 4 bits, rampe de couleurs).
    venv/bin/python p600/make_splash.py p600/fonts/vimongrong/MONRON1T.TTF p600/splash ../Felucca/firmware/src/p600_splash.h"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Felucca", "tools"))
import lz4blk                                                  # (10/11 : les images compressées sans perte, LZ4)

BG, FG, SUB = (12, 11, 10), (238, 232, 216), (214, 84, 64)    # noir du panneau, crème du logo, rouge de la mention
CREDC = (168, 162, 150)                                        # le crédit Felucca : plus discret, lisible
VERC = (206, 200, 186)                                         # le numéro de version : gris crème, lisible
WAVE = (255, 64, 48)                                           # l'onde : le rouge de l'afficheur LED du Prophet
SS = 4                                                         # suréchantillonnage
VERSION = "1.0.1"                                              # la version de Guru 600, sous la mention


def text_img(font_path, text, px, pad=2):
    f = ImageFont.truetype(font_path, px * SS)
    l, t, r, b = f.getbbox(text)
    im = Image.new("L", (r - l + 2 * pad * SS, b - t + 2 * pad * SS), 0)
    ImageDraw.Draw(im).text((pad * SS - l, pad * SS - t), text, font=f, fill=255)
    return im.resize((im.width // SS, im.height // SS), Image.LANCZOS)


def text_direct(font_path, text, px, pad=2):   # drawn at its size by FreeType (hinted): crisp, no resampling
    f = ImageFont.truetype(font_path, px)
    l, t, r, b = f.getbbox(text)
    im = Image.new("L", (r - l + 2 * pad, b - t + 2 * pad), 0)
    ImageDraw.Draw(im).text((pad - l, pad - t), text, font=f, fill=255)
    return im


INTER = os.path.expanduser("~/Documents/FM-1/Felucca/assets/fonts/InterTight[wght].ttf")


def tracked(text, px, weight, track):       # du texte Inter Tight à la graisse donnée, lettres espacées de track px
    f = ImageFont.truetype(INTER, px * SS)
    f.set_variation_by_axes([weight])
    w = sum(f.getlength(c) for c in text) + track * SS * (len(text) - 1)
    l, t, r, b = f.getbbox(text)
    im = Image.new("L", (int(w) + 4 * SS, b - t + 4 * SS), 0)
    d, x = ImageDraw.Draw(im), 2 * SS
    for c in text:
        d.text((x, 2 * SS - t), c, font=f, fill=255)
        x += f.getlength(c) + track * SS
    return im.resize((im.width // SS, im.height // SS), Image.LANCZOS)


def main(font, outdir, header):
    logo = text_direct(font, "guru-600", 54)      # VI Mong Rong (VN-Fonts Team, 1994: free to use and share)
    sub = tracked("A PROPHET-600 TRIBUTE", 13, 800, 1.2)   # la typo des cadres (Inter Tight ExtraBold), espacée
    ver = tracked("by Marc Massé, v" + VERSION, 11, 450, 0.2)   # Inter Tight aussi, en graisse normale
    cred = tracked("based on Felucca by Leo Kuroshita", 9, 400, 0.3)   # le crédit du firmware de base, en petit
    W = 240
    canvas = Image.new("L", (W, 240), 0)
    canvas_sub = Image.new("L", (W, 240), 0)
    y = (240 - logo.height) // 2 - 8
    canvas.paste(logo, ((W - logo.width) // 2, y))
    canvas_sub.paste(sub, ((W - sub.width) // 2, y + logo.height + 18))
    prev = Image.new("RGB", (W, 240), BG)
    prev.paste(Image.new("RGB", (W, 240), FG), mask=canvas)
    prev.paste(Image.new("RGB", (W, 240), SUB), mask=canvas_sub)
    prev.resize((W * 3, 720), Image.NEAREST).save(f"{outdir}/splash_preview.png")

    # en-tête : les deux zones (logo, mention) en alpha 4 bits, rangées de pixels
    def ramp(fg):
        out = []
        for k in range(16):
            c = [round(BG[i] + (fg[i] - BG[i]) * k / 15) for i in range(3)]
            v = ((c[0] >> 3) << 11) | ((c[1] >> 2) << 5) | (c[2] >> 3)
            out.append(((v & 255) << 8) | (v >> 8))            # octets inversés : l'écran prend le RGB565 gros-boutiste
        return out

    def packed(im):
        a = [round(p * 15 / 255) for p in im.get_flattened_data()]
        if len(a) % 2:
            a.append(0)
        return [a[i] | a[i + 1] << 4 for i in range(0, len(a), 2)]

    L = ["/* SPDX-License-Identifier: GPL-3.0-only */",
         "/* The power-on screen « Guru~600 » (ui_draw.c draw_splash): made by p600/make_splash.py, do not edit. Alpha 4 bits a",
         " * pixel (two a byte, low nibble first), coloured through a 16-step ramp from the panel's black (byte-swapped RGB565).",
         " * Each area's alpha is kept LZ4-compressed (SPL_x_Z, lossless; its size unpacked SPL_x_N) and unpacked at power-on",
         " * into the canvas, free while the splash runs (ui_draw.c splash_unpack): SPL_x_A points there */"]
    Z = []
    v = ramp(FG)[0]
    L.append("static const uint16_t SPL_BG = 0x%04X;   /* (lcd_fill takes it as the theme's colours: in order) */" %
             (((v & 255) << 8) | (v >> 8)))
    for name, im, col, x, yy in (("LOGO", logo, FG, (W - logo.width) // 2, y),
                                 ("SUB", sub, SUB, (W - sub.width) // 2, y + logo.height + 18),
                                 ("VER", ver, VERC, (W - ver.width) // 2, y + logo.height + 18 + sub.height + 6),
                                 ("CRED", cred, CREDC, (W - cred.width) // 2,
                                  y + logo.height + 18 + sub.height + 6 + ver.height + 4)):
        L.append("#define SPL_%s_X %d\n#define SPL_%s_Y %d\n#define SPL_%s_W %d\n#define SPL_%s_H %d" %
                 (name, x, name, yy, name, im.width, name, im.height))
        L.append("static const uint16_t SPL_%s_RAMP[16] = {%s};" % (name, ", ".join("0x%04X" % v for v in ramp(col))))
        if name == "LOGO":                                 # le reflet qui passe sur les lettres (animation)
            L.append("static const uint16_t SPL_GLINT_RAMP[16] = {%s};" %
                     ", ".join("0x%04X" % v for v in ramp((255, 252, 244))))
            L.append("static const uint16_t SPL_WAVE_RAMP[16] = {%s};" % ", ".join("0x%04X" % v for v in ramp(WAVE)))
        d = packed(im)
        z = lz4blk.compress(bytes(d))
        assert lz4blk.decompress(z) == bytes(d)                # (sans perte : vérifié)
        Z.append((name, len(d), len(z)))
        L.append("#define SPL_%s_N %d" % (name, len(d)))
        L.append("static const uint8_t SPL_%s_Z[%d] = {" % (name, len(z)))
        for i in range(0, len(z), 24):
            L.append("    " + ", ".join(str(b) for b in z[i:i + 24]) + ",")
        L.append("};")
    L.append("static const uint8_t *const SPL_Z[%d] = {%s};" % (len(Z), ", ".join("SPL_%s_Z" % n for n, _, _ in Z)))
    L.append("static const uint16_t SPL_ZN[%d][2] = {%s};   /* packed, unpacked */" %
             (len(Z), ", ".join("{%d, %d}" % (b, a) for _, a, b in Z)))
    L.append("static const uint8_t *spl_a[%d];   /* the unpacked areas (in the canvas, during the splash) */" % len(Z))
    for k, (n, _, _) in enumerate(Z):
        L.append("#define SPL_%s_A (spl_a[%d])" % (n, k))
    open(header, "w").write("\n".join(L) + "\n")
    print("compressé :", ", ".join("%s %d -> %d" % z for z in Z))
    print("logo", logo.size, "mention", sub.size, "->", header)


if __name__ == "__main__":
    main(*sys.argv[1:4])
