#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2026 Leo Kuroshita (@kurogedelic), Hügelton Instruments
"""Smooth lookup tables stored packed in flash, unpacked once at boot into RAM (gen_tables.py, gen_uac_fir.py).

A table of n values (8, 16 or 32 bits) is kept as its first k * st values (4 bytes each, little-endian) and, for
every later value, the w-bit two's complement residual of the k-th order polynomial prediction along stride st:
    x[i] = r[i] + sum_j (-1)^(j+1) C(k, j) x[i - j st]      (mod 2^bits: exact; j = 1 .. k)
the residuals LSB first, back to back. k, st and w are chosen per table (the smallest blob); the decoder is
emulated here and must give back every value, bit for bit, or the build stops.

The table itself becomes a RAM array (TAB_RAM): on the target in .ramtab (firmware/app.ld: RAMTEXT after the
second core's loop, NOLOAD), filled by tab_init_<header>() from fm1_cstart (src/main.c) before anything reads
it; on a host (tests, the web emulator) a constructor fills it before main (spelled __attribute, not
__attribute__: tests/hostsim.c defines __attribute__ away), and tab_init_<header>() may be called again (once
only). The C decoder is TAB_UNPACK_C below (one copy for every header)."""
import re
from math import comb

SZ = {"int8_t": 1, "uint8_t": 1, "int16_t": 2, "uint16_t": 2, "int32_t": 4, "uint32_t": 4}

TAB_UNPACK_C = r"""#ifndef TAB_UNPACK_DEFINED   /* (tools/tabpack.py: one copy for every header that holds packed tables) */
#define TAB_UNPACK_DEFINED
#ifdef __PI32V2__
#define TAB_RAM __attribute__((section(".ramtab")))   /* app.ld: RAMTEXT, after .c1_text; filled by fm1_cstart */
#define TAB_HOST_INIT
#else
#define TAB_RAM
#define TAB_HOST_INIT __attribute((constructor))     /* (__attribute: hostsim.c defines __attribute__ away) */
#endif
typedef struct { void *dst; const uint8_t *z; uint16_t n; uint8_t sz, st, k, w; } tab_pack_t;
/* every table of d[0 .. cnt - 1]: its first k * st values as they are, then each the w-bit residual (LSB first)
 * plus the k-th order prediction from the values k, k - 1 .. 1 strides back (binomial coefficients), mod 2^(8 sz) */
static __attribute__((noinline)) void tab_unpack(const tab_pack_t *d, uint32_t cnt)
{
    static const int8_t C[6][5] = {{0}, {1}, {2, -1}, {3, -3, 1}, {4, -6, 4, -1}, {5, -10, 10, -5, 1}};
    for (; cnt--; d++) {
        uint32_t i, j, pos = 0, h = (uint32_t)d->k * d->st, w = d->w;
        const uint8_t *z = d->z, *bits = z + 4u * h;
        for (i = 0; i < d->n; i++) {
            uint32_t v;
            if (i < h) {
                v = (uint32_t)z[4u * i] | (uint32_t)z[4u * i + 1u] << 8 | (uint32_t)z[4u * i + 2u] << 16 |
                    (uint32_t)z[4u * i + 3u] << 24;
            } else {
                uint32_t b;
                for (v = 0, b = 0; b < w; b++, pos++)
                    v |= (uint32_t)((bits[pos >> 3] >> (pos & 7u)) & 1u) << b;
                if (v >> (w - 1u))
                    v |= ~0u << (w - 1u) << 1;
                for (j = 1; j <= d->k; j++) {
                    uint32_t a = i - j * d->st;
                    uint32_t x = d->sz == 4u ? ((const uint32_t *)d->dst)[a] :
                                 d->sz == 2u ? ((const uint16_t *)d->dst)[a] : ((const uint8_t *)d->dst)[a];
                    v += (uint32_t)(int32_t)C[d->k][j - 1u] * x;
                }
            }
            if (d->sz == 4u)
                ((uint32_t *)d->dst)[i] = v;
            else if (d->sz == 2u)
                ((uint16_t *)d->dst)[i] = (uint16_t)v;
            else
                ((uint8_t *)d->dst)[i] = (uint8_t)v;
        }
    }
}
#endif
"""


def _predict(v, i, st, k):
    return sum((-1) ** (j + 1) * comb(k, j) * v[i - j * st] for j in range(1, k + 1))


def _emulate(nbits, n, st, k, w, blob):
    """the C decoder (TAB_UNPACK_C)"""
    mask, h = (1 << nbits) - 1, k * st
    d = [int.from_bytes(blob[4 * i:4 * i + 4], "little") & mask for i in range(h)] + [0] * (n - h)
    bits, pos = blob[4 * h:], 0
    for i in range(h, n):
        r = sum(((bits[(pos + b) >> 3] >> ((pos + b) & 7)) & 1) << b for b in range(w))
        pos += w
        if r >> (w - 1):
            r -= 1 << w
        d[i] = (r + _predict(d, i, st, k)) & mask
    return d


def pack(ctype, vals, strides):
    """-> (blob, st, k, w): the smallest packing of vals over the strides offered and orders 0 .. 5"""
    best = None
    for st in strides:
        for k in range(6):
            if k * st >= len(vals):
                continue
            res = [vals[i] - _predict(vals, i, st, k) for i in range(k * st, len(vals))]
            w = max(max(r.bit_length() + 1 if r >= 0 else (-r - 1).bit_length() + 1 for r in res), 1)
            size = 4 * k * st + (len(res) * w + 7) // 8
            if best is None or size < best[0]:
                best = (size, st, k, w, res)
    _, st, k, w, res = best
    blob = bytearray(b"".join((v & 0xFFFFFFFF).to_bytes(4, "little") for v in vals[:k * st]))
    acc = nb = 0
    for r in res:
        acc |= (r & ((1 << w) - 1)) << nb
        nb += w
        while nb >= 8:
            blob.append(acc & 255)
            acc >>= 8
            nb -= 8
    if nb:
        blob.append(acc & 255)
    nbits = 8 * SZ[ctype]
    assert _emulate(nbits, len(vals), st, k, w, blob) == [v & ((1 << nbits) - 1) for v in vals], "tabpack: decode"
    assert w <= 32 and st < 256 and len(vals) < 65536
    return bytes(blob), st, k, w


def rewrite(text, names, init):
    """the C text with each table of names (static const T NAME[a][b].. = {..};) packed; adds TAB_UNPACK_C, the
    descriptors and `static void init(void)` (idempotent; a constructor on a host). Returns (text, report)"""
    descs, report = [], []
    for name in names:
        m = re.search(r"static const (u?int(?:8|16|32)_t) " + name + r"((?:\[\w+\])+) = \{(.*?)\};", text, re.S)
        if not m:
            raise SystemExit(f"tabpack: no table {name}")
        ctype, dims, body = m.groups()
        vals = [int(x, 0) for x in re.findall(r"-?(?:0x[0-9a-fA-F]+|\d+)", re.sub(r"/\*.*?\*/", "", body))]
        dl = [int(x) for x in re.findall(r"\[(\d+)\]", dims)]
        n = 1
        for x in dl:
            n *= x
        assert n == len(vals), f"tabpack: {name} has {len(vals)} values, not {n}"
        blob, st, k, w = pack(ctype, vals, [1] + ([dl[-1]] if len(dl) > 1 else []))
        new = (f"static {ctype} {name}{dims} TAB_RAM;   /* (tools/tabpack.py: {name}_Z unpacked at boot) */\n"
               + "\n".join([f"static const uint8_t {name}_Z[{len(blob)}] = {{"] +
                           ["    " + ", ".join(str(b) for b in blob[i:i + 24]) + "," for i in range(0, len(blob), 24)] +
                           ["};"]))
        text = text[:m.start()] + new + text[m.end():]
        descs.append(f"    {{(void *){name}, {name}_Z, {n}u, {SZ[ctype]}u, {st}u, {k}u, {w}u}},")
        report.append(f"{name} {n * SZ[ctype]} -> {len(blob)} B (stride {st}, order {k}, {w} bits)")
    tail = ["", f"/* tools/tabpack.py: the packed tables above, unpacked once (src/main.c fm1_cstart; a host: before main) */",
            f"static const tab_pack_t {init.upper()}_TABS[] = {{", *descs, "};",
            f"static TAB_HOST_INIT void {init}(void)", "{", "    static uint8_t done;", "    if (!done) {",
            "        done = 1;", f"        tab_unpack({init.upper()}_TABS, {len(descs)}u);", "    }", "}", ""]
    m = re.search(r"#include <stdint.h>\n", text)
    pos = m.end() if m else 0
    text = text[:pos] + ("" if m else "#include <stdint.h>\n") + TAB_UNPACK_C + text[pos:] + "\n".join(tail)
    return text, report
