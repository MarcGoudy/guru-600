"""L'écran d'installation du Guru-600 (le chargeur : Felucca/firmware/loader/ldr_screen.c) : ses images.
  - le logo « guru-600 » de l'écran d'accueil (VI Mong Rong, 54 px) : il sert de barre de progression, blanc cassé foncé,
    rempli de gauche à droite en crème au fil de l'écriture (idée de Marc, 15/11) ; en attente, un reflet le parcourt ;
  - les textes en Guru600, la police dessinée par Marc (titres du site et de l'éditeur ; fonts/guru600/Guru600.ttf,
    reconstruite depuis son dessin par l'outil du site, sans crénage) : UPDATE MODE, WRITING, UPDATE FAILED, ce qu'il
    faut faire, l'adresse du site guru-600.com ;
  - les chiffres et % du pourcentage, sous le logo, en Guru600 aussi, tous dans une case de même largeur.
Alpha 4 bits (deux pixels par octet, le bas d'abord) ; les rampes (16 couleurs, du fond à la couleur, RGB565 aux octets
inversés) sont dans le même en-tête.
    venv/bin/python p600/make_ldr_screen.py p600/fonts/vimongrong/MONRON1T.TTF ../Felucca/firmware/loader/ldr_art.h [aperçu.png]"""
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_splash                                             # text_direct, tracked, INTER, FG : comme au démarrage

BG = (0x15, 0x12, 0x13)                                        # le fond (celui du chargeur jusqu'ici)
CREAM = make_splash.FG                                         # le logo rempli, les titres
DIM = (78, 72, 66)                                             # le logo à remplir : blanc cassé foncé
LIGHT = (255, 255, 255)                                        # le cœur du reflet : blanc (Marc, 15/11)
GLOW = (255, 255, 255)                                         # la lumière du halo : blanche (Marc, 15/11)
GREY = (168, 162, 150)                                         # ce qu'il faut faire, l'adresse
RED = make_splash.SUB                                          # UPDATE FAILED : le rouge de la mention
SS = 4
GURU = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts", "guru600", "Guru600.ttf")


def tracked(text, px, track):                                  # du texte Guru600, lettres espacées de track px
    f = ImageFont.truetype(GURU, px * SS)
    w = sum(f.getlength(c) for c in text) + track * SS * (len(text) - 1)
    l, t, r, b = f.getbbox(text)
    im = Image.new("L", (int(w) + 4 * SS, b - t + 4 * SS), 0)
    d, x = ImageDraw.Draw(im), 2 * SS
    for c in text:
        d.text((x, 2 * SS - t), c, font=f, fill=255)
        x += f.getlength(c) + track * SS
    im = im.resize((im.width // SS, im.height // SS), Image.LANCZOS)
    return im.crop(im.getbbox())


def rgb565s(c):
    v = ((c[0] >> 3) << 11) | ((c[1] >> 2) << 5) | (c[2] >> 3)
    return ((v & 255) << 8) | (v >> 8)


def ramp(col):
    return [rgb565s([round(BG[i] + (col[i] - BG[i]) * k / 15) for i in range(3)]) for k in range(16)]


def packed(im):
    a = [round(p * 15 / 255) for p in im.get_flattened_data()]
    if len(a) % 2:
        a.append(0)
    return [a[i] | a[i + 1] << 4 for i in range(0, len(a), 2)]


def digits(px):
    """0..9 et %, chacun dans une case de même largeur et de même hauteur (même ligne de base)."""
    f = ImageFont.truetype(GURU, px * SS)
    chars = "0123456789%"
    boxes = [f.getbbox(c) for c in chars]
    top, bot = min(b[1] for b in boxes), max(b[3] for b in boxes)
    w = max(f.getlength(c) for c in chars[:10])                    # (les chiffres : la case du plus large)
    cells = []
    for c in chars:
        cw = max(w, f.getlength(c))
        im = Image.new("L", (int(cw) + 2 * SS, bot - top + 2 * SS), 0)
        ImageDraw.Draw(im).text(((im.width - f.getlength(c)) / 2, SS - top), c, font=f, fill=255)
        cells.append(im.resize((im.width // SS, im.height // SS), Image.LANCZOS))
    return cells


def main(font, header, preview=None):
    logo = make_splash.text_direct(font, "guru-600", 54, pad=6)   # (6 px autour : la place du halo)
    # (le halo du reflet : calculé par le chargeur à l'allumage, ldr_screen.c ldr_halo_make, pour la place)
    T = tracked
    texts = [("MODE", T("UPDATE MODE", 17, 0.8)), ("WRITING", T("WRITING", 17, 0.8)),
             ("FAILED", T("UPDATE FAILED", 17, 0.8)), ("WAIT", T("WAITING FOR THE INSTALL", 11, 0.6)),
             ("NOOFF", T("DO NOT SWITCH OFF", 11, 0.6)), ("AGAIN", T("INSTALL AGAIN", 11, 0.6)),
             ("SITE", T("guru-600.com", 10, 0.5)), ("VER", T("v" + make_splash.VERSION, 13, 0.6))]
    cells = digits(22)                                             # (Marc, 15/11 : sous le logo, calé à sa droite)
    L = ["/* SPDX-License-Identifier: GPL-3.0-only */",
         "/* The update loader's screen (ldr_screen.c): made by p600/make_ldr_screen.py, do not edit. The power-on screen's",
         " * « guru-600 » logo (VI Mong Rong, VN-Fonts Team 1994, free to use and share), the progress bar itself; the texts and",
         " * the percent in Guru600 (Marc Massé's own typeface). Alpha 4 bits a pixel (two a byte, low nibble first), coloured through",
         " * 16-step ramps from the background (byte-swapped RGB565). All in the loader: the app area may be half written */",
         "#define LA_BG 0x%04Xu   /* (as lcd_fill takes it: in order) */" % rgb565s(BG)[::1] if False else
         "#define LA_BG 0x%04Xu   /* (as lcd_fill takes it: in order) */" % (((rgb565s(BG) & 255) << 8) | (rgb565s(BG) >> 8))]
    for name, col in (("DIM", DIM), ("FULL", CREAM), ("INK", CREAM), ("SUB", GREY), ("RED", RED)):
        L.append("static const uint16_t LA_R_%s[16] = {%s};" % (name, ", ".join("0x%04X" % v for v in ramp(col))))
    # le reflet : les lettres éclaircies vers LIGHT, comme au démarrage (SPL_GLINT_RAMP) ; le halo y ajoute GLOW
    L.append("static const uint16_t LA_R_LIGHT[16] = {%s};" % ", ".join("0x%04X" % v for v in ramp(LIGHT)))
    total = 0

    def arr(name, im):
        nonlocal total
        d = packed(im)
        total += len(d)
        L.append("#define LA_%s_W %du\n#define LA_%s_H %du" % (name, im.width, name, im.height))
        L.append("static const uint8_t LA_%s[%d] = {" % (name, len(d)))
        for i in range(0, len(d), 32):
            L.append("    " + ",".join(str(b) for b in d[i:i + 32]) + ",")
        L.append("};")

    arr("LOGO", logo)
    L.append("static const uint16_t LA_GLOW = 0x%04X;   /* the glow's light (plain RGB565) */" % (((GLOW[0] >> 3) << 11) | ((GLOW[1] >> 2) << 5) | (GLOW[2] >> 3)))
    for n, im in texts:
        arr(n, im)
    for k, im in enumerate(cells):
        arr("D%d" % k, im)
    L.append("static const uint8_t *const LA_DIG[11] = {%s};" % ", ".join("LA_D%d" % k for k in range(11)))
    L.append("static const uint8_t LA_DIG_W[11] = {%s};" % ", ".join("LA_D%d_W" % k for k in range(11)))
    L.append("#define LA_DIG_H LA_D0_H")
    L.append('#define LA_VERSION "%s"   /* the version drawn (LA_VER): guru_version.h when it was made */' % make_splash.VERSION)
    L.append("#define LA_LOGO_INK_L %du   /* the logo's ink starts here: the version under it, ranged left */" % logo.getbbox()[0])
    # le pourcentage calé à droite sur le logo : le bord droit de l'encre du logo, celui de l'encre du %
    L.append("#define LA_LOGO_INK_R %du   /* the logo's ink ends here (its last column + 1) */" % logo.getbbox()[2])
    L.append("#define LA_PCT_INK_R %du    /* the %% cell's ink ends here */" % cells[10].getbbox()[2])
    open(header, "w").write("\n".join(L) + "\n")
    print("ldr_art :", total, "octets d'images ->", header)
    if preview:                                                    # l'écran à 57 %, comme le chargeur le dessine
        pv = Image.new("RGB", (240, 240), BG)

        def put(im, x, y, col, clip=None):
            m = im if clip is None else im.crop((0, 0, clip, im.height))
            pv.paste(Image.new("RGB", m.size, col), (x, y), m)
        put(logo, (240 - logo.width) // 2, 42, DIM)
        put(logo, (240 - logo.width) // 2, 42, CREAM, int(logo.width * .57))
        s = [cells[5], cells[7], cells[10]]
        x = (240 - logo.width) // 2 + logo.getbbox()[2] - cells[10].getbbox()[2] - sum(c.width for c in s[:-1])
        for c in s:
            put(c, x, 94, CREAM); x += c.width
        put(texts[1][1], (240 - texts[1][1].width) // 2, 158, CREAM)
        put(texts[4][1], (240 - texts[4][1].width) // 2, 180, GREY)
        put(texts[6][1], (240 - texts[6][1].width) // 2, 222, GREY)
        pv.resize((720, 720), Image.NEAREST).save(preview)


if __name__ == "__main__":
    main(*sys.argv[1:4])
