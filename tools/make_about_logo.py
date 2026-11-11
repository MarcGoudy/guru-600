"""Logo « Guru~600 » de MENU > ABOUT : le logo de l'écran de démarrage (p600_splash.h, SPL_LOGO), en taille réelle,
recodé en Huffman comme les glyphes des polices (gfx.c cv_alpha_hc) : 1,2 Ko au lieu des 4,7 Ko de l'alpha brut.
    venv/bin/python p600/make_about_logo.py ../Felucca/firmware/src/p600_splash.h ../Felucca/firmware/src/p600_about.h
(depuis le dossier FM-1 : les outils de Felucca, gen_aa_font.py, sont pris dans ../Felucca/tools ou Felucca/tools)"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
for t in (os.path.join(HERE, "..", "Felucca", "tools"), os.path.join(HERE, "..", "firmware", "tools")):
    if os.path.isdir(t):
        sys.path.insert(0, t)
from gen_aa_font import huff_pack, huff_unpack   # noqa: E402


def lz4_block(src, n):
    """un bloc LZ4 (sans en-tête de trame) -> n octets"""
    out, i = bytearray(), 0
    while i < len(src):
        t = src[i]
        i += 1
        lit = t >> 4
        if lit == 15:
            while True:
                b = src[i]
                i += 1
                lit += b
                if b != 255:
                    break
        out += src[i:i + lit]
        i += lit
        if i >= len(src):
            break
        off = src[i] | src[i + 1] << 8
        i += 2
        m = t & 15
        if m == 15:
            while True:
                b = src[i]
                i += 1
                m += b
                if b != 255:
                    break
        for _ in range(m + 4):
            out.append(out[-off])
    return bytes(out[:n])


def main(splash_h, about_h):
    h = open(splash_h, encoding="utf-8").read()
    w = int(re.search(r"#define SPL_LOGO_W (\d+)", h).group(1))
    hh = int(re.search(r"#define SPL_LOGO_H (\d+)", h).group(1))
    n = int(re.search(r"#define SPL_LOGO_N (\d+)", h).group(1))
    z = bytes(int(x) for x in re.search(r"SPL_LOGO_Z\[\d+\] = \{(.*?)\};", h, re.S).group(1).split(",") if x.strip())
    raw = lz4_block(z, n)
    vals = [(raw[k >> 1] >> ((k & 1) * 4)) & 15 for k in range(w * hh)]   # (bas de l'octet d'abord, comme le splash)
    hc, d = huff_pack([vals])
    data = d[0] + b"\0\0"                                                 # (cv_alpha_hc lit 2 octets d'avance)
    assert huff_unpack(hc, data, len(vals)) == vals

    def fmt(b):
        return ",\n    ".join(", ".join(str(x) for x in b[i:i + 24]) for i in range(0, len(b), 24))
    open(about_h, "w", encoding="utf-8").write(f"""/* SPDX-License-Identifier: GPL-3.0-only */
/* MENU > ABOUT: the « Guru~600 » logo of the power-on screen (p600_splash.h SPL_LOGO), {w} x {hh}, its 4-bit alpha
 * Huffman-coded like the fonts' glyphs (gfx.c cv_alpha_hc; made by p600/make_about_logo.py, do not edit) */
#define ABOUT_LOGO_W {w}
#define ABOUT_LOGO_H {hh}
static const uint8_t ABOUT_LOGO_HC[{len(hc)}] = {{
    {fmt(bytes(hc))}}};
static const uint8_t ABOUT_LOGO_D[{len(data)}] = {{
    {fmt(data)}}};
""")
    print(f"logo {w} x {hh} : {len(hc) + len(data)} octets -> {about_h}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
