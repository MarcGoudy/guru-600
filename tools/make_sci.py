"""Les 100 programmes d'usine du Prophet-600 tels que Sequential les envoie (16 octets chacun), pour l'export exact
d'un son d'usine non modifié : Felucca/firmware/src/p600_sci.h.
    venv/bin/python p600/make_sci.py "matrix12x-p600fw/Prophet-600 factory patches.syx" Felucca/firmware/src/p600_sci.h"""
import sys
d = open(sys.argv[1], "rb").read()
msgs, i = [], 0
while i < len(d):
    if d[i] == 0xF0:
        j = d.index(0xF7, i); msgs.append(d[i + 1:j]); i = j + 1
    else:
        i += 1
assert len(msgs) == 100 and all(len(m) == 35 and m[0] == 1 and m[1] == 2 for m in msgs)
L = ["/* SPDX-License-Identifier: GPL-3.0-only */",
     "/* The Prophet-600's 100 factory programs as Sequential's dump holds them (the Z80's 16 bytes each), for an exact",
     " * export of an unmodified factory sound (eng_p600.c p600_export). Made by p600/make_sci.py: do not edit */",
     "static const uint8_t P6_SCI_FACT[100][16] = {"]
for m in msgs:
    b = [(m[3 + 2 * k] & 15) | (m[4 + 2 * k] & 15) << 4 for k in range(16)]
    L.append("    {" + ", ".join(str(x) for x in b) + "},")
L.append("};")
open(sys.argv[2], "w").write("\n".join(L) + "\n")
print(sys.argv[2])
