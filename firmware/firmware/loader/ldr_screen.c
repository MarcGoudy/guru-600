/* SPDX-License-Identifier: GPL-3.0-only
 * Copyright (C) 2026 zvenson (Shine On: the loader's screen this one started from)
 * Copyright (C) 2026 illuminus5 (Skiff: the idea, a loader that draws, and the order of things)
 * Copyright (C) 2026 Marc Massé (Guru-600: the logo as the progress bar, the look) */
/* The update loader's screen (loader.c; tests/ldr_screen_test.c). A unit whose install was cut off comes back to the
 * loader at every power-on and showed a black screen; now it says what it does. Guru-600's own look (Marc, 15/11):
 *   the power-on screen's « guru-600 » logo is the progress bar: dark off-white, filled in cream from left to right as
 *   it writes, a glow at its edge; while it waits, a slanted glint with its glow runs through it (ldr_anim); written,
 *   one last glint over it (ldr_done)
 *   under it, on the left the version it installs, on the right the percent, ranged on the logo's right edge (Guru600, Marc Massé's typeface, as the texts)
 *   what happens (UPDATE MODE, WRITING, UPDATE FAILED: red) and what to do, cream and grey
 *   guru-600.com at the foot: where the guide and the installer are
 * Every image is in the loader (ldr_art.h, p600/make_ldr_screen.py: the app area may be half written, never read),
 * drawn before USB starts (USB is polled: the panel's ~0.3 s init would leave the host's enumeration unanswered).
 * FM-1 only (the SMK-37's stays dark). */
#define LDR_LOGO_Y 42u                      /* (its image has 6 px around the letters: the glow's room) */
#define LDR_PCT_Y 94u                       /* (Marc, 15/11: under the logo, on its right edge) */
#define LDR_SAY_Y 158u
#define LDR_SUB_Y 180u
#define LDR_SITE_Y 222u
#define LDR_GLINT 14                                /* the glint: 14 px each side of its line, as at power-on */
#define LDR_SLANT (LA_LOGO_H / 2)                   /* its slant: the bottom row this far left of the top one */
#define LDR_EDGE 7                                  /* the glow at the fill's edge, while it writes */

static uint16_t ldr_row[240];
static uint16_t ldr_sw(uint32_t c) { return (uint16_t)((c >> 8 | c << 8) & 0xFFFFu); }   /* (the panel's byte order) */
static uint16_t ldr_add(uint16_t sc, uint32_t g)    /* a swapped colour plus the glow's light, g 0..256 */
{
    uint32_t c = ldr_sw(sc), r = (c >> 11) + ((LA_GLOW >> 11) * g >> 8), gg = (c >> 5 & 63u) + ((LA_GLOW >> 5 & 63u) * g >> 8),
             b = (c & 31u) + ((LA_GLOW & 31u) * g >> 8);
    return ldr_sw((r > 31u ? 31u : r) << 11 | (gg > 63u ? 63u : gg) << 5 | (b > 31u ? 31u : b));
}
/* an image (alpha 4 bits) at x, y through a ramp, row by row (the texts, the digits) */
static void ldr_blit(uint32_t x, uint32_t y, uint32_t w, uint32_t h, const uint8_t *d, const uint16_t *rp)
{
    uint32_t r, i, a;
    for (r = 0; r < h; r++) {
        lcd_sync();                                 /* (the row before is sent: its buffer is free) */
        for (i = 0; i < w; i++) {
            a = r * w + i;
            ldr_row[i] = rp[d[a >> 1] >> ((a & 1u) * 4u) & 15u];
        }
        lcd_blit(x, y + r, w, 1, ldr_row);
    }
}
#define LDR_IMG(n, y, r) ldr_blit((240u - LA_##n##_W) / 2u, (y), LA_##n##_W, LA_##n##_H, LA_##n, (r))

static uint32_t ldr_fill;                           /* logo columns filled (0..LA_LOGO_W) */
static uint32_t ldr_pct = 0xFFFFu;                  /* the percent on the screen, 0xFFFF none */
static uint8_t ldr_writing;                         /* WRITING is on the screen */
static uint8_t ldr_idle = 1;                        /* the glint runs (not after a write, nor a failure) */
#define LDR_GX0 (-LDR_GLINT - LDR_SLANT)            /* (the glint's line, at the top row: off the logo on the left) */
static int32_t ldr_gx = LDR_GX0;                    /* the glint's line at the top row, in logo columns; LDR_GX0 none */
static uint32_t ldr_next;                           /* its next move */

/* the glow's halo: the logo blurred (three box blurs of 9 px across, then down: about a Gaussian of 4.5 px), made
 * once at power-on in RAM rather than kept in the loader (Marc, 15/11: room) */
static uint8_t ldr_halo[LA_LOGO_W * LA_LOGO_H];
static void ldr_blur(uint8_t *p, uint32_t n, uint32_t step)   /* one box blur of 9 along a line of n, in place */
{
    uint8_t c[LA_LOGO_W > LA_LOGO_H ? LA_LOGO_W : LA_LOGO_H];
    uint32_t i, s = 0;
    for (i = 0; i < n; i++)
        c[i] = p[i * step];
    for (i = 0; i < 4u && i < n; i++)
        s += c[i];
    for (i = 0; i < n; i++) {
        if (i + 4u < n)
            s += c[i + 4u];
        p[i * step] = (uint8_t)(s / 9u);
        if (i >= 4u)
            s -= c[i - 4u];
    }
}
static void ldr_halo_make(void)
{
    uint32_t i, k, mx = 1;
    for (i = 0; i < LA_LOGO_W * LA_LOGO_H; i++)
        ldr_halo[i] = (uint8_t)((LA_LOGO[i >> 1] >> ((i & 1u) * 4u) & 15u) * 17u);
    for (k = 0; k < 3u; k++) {
        for (i = 0; i < LA_LOGO_H; i++)
            ldr_blur(ldr_halo + i * LA_LOGO_W, LA_LOGO_W, 1);
        for (i = 0; i < LA_LOGO_W; i++)
            ldr_blur(ldr_halo + i, LA_LOGO_H, LA_LOGO_W);
    }
    for (i = 0; i < LA_LOGO_W * LA_LOGO_H; i++)
        mx = ldr_halo[i] > mx ? ldr_halo[i] : mx;
    for (i = 0; i < LA_LOGO_W * LA_LOGO_H; i++)
        ldr_halo[i] = (uint8_t)(ldr_halo[i] * 255u / mx);
}
/* the logo, the progress bar: columns < ldr_fill cream, the others dark off-white; the glint (ldr_gx, slanted: the
 * letters lit as at power-on, and the glow, its halo ldr_halo, on the black around them); at the fill's edge while it
 * writes, a glow too */
static void ldr_logo(void)
{
    uint32_t r, i, p, la, hl, k;
    int32_t d, line;
    for (r = 0; r < LA_LOGO_H; r++) {
        lcd_sync();
        line = ldr_gx + (int32_t)(LA_LOGO_H - 1u - r) * LDR_SLANT / (int32_t)LA_LOGO_H;   /* (slanted: / ) */
        for (i = 0; i < LA_LOGO_W; i++) {
            p = r * LA_LOGO_W + i;
            la = LA_LOGO[p >> 1] >> ((p & 1u) * 4u) & 15u;
            hl = ldr_halo[p];
            ldr_row[i] = (i < ldr_fill ? LA_R_FULL : LA_R_DIM)[la];
            k = 0;
            d = (int32_t)i - line;
            if (ldr_gx != LDR_GX0 && d > -LDR_GLINT && d < LDR_GLINT)
                k = (uint32_t)(LDR_GLINT - (d < 0 ? -d : d)) * 256u / LDR_GLINT;    /* 0..256, its middle 256 */
            d = (int32_t)ldr_fill - 1 - (int32_t)i;
            if (ldr_writing && ldr_fill < LA_LOGO_W && d >= 0 && d < LDR_EDGE && k < (uint32_t)(LDR_EDGE - d) * 160u / LDR_EDGE)
                k = (uint32_t)(LDR_EDGE - d) * 160u / LDR_EDGE;                 /* (the edge: softer) */
            if (k) {
                if (la)                             /* the letters lit (ui_draw.c's glint) */
                    ldr_row[i] = LA_R_LIGHT[la + (k * (15u - la) >> 8)];
                ldr_row[i] = ldr_add(ldr_row[i], hl * k * 240u / (255u * 256u));    /* the glow, its halo */
            }
        }
        lcd_blit((240u - LA_LOGO_W) / 2u, LDR_LOGO_Y + r, LA_LOGO_W, 1, ldr_row);
    }
}
/* the status (0 UPDATE MODE, 1 WRITING, 2 UPDATE FAILED) and what to do */
static void ldr_say(uint32_t k)
{
    lcd_fill(0, LDR_SAY_Y, 240, LDR_SITE_Y - 8u - LDR_SAY_Y, LA_BG);
    if (k == 0u) {
        LDR_IMG(MODE, LDR_SAY_Y, LA_R_INK);
        LDR_IMG(WAIT, LDR_SUB_Y, LA_R_SUB);
    } else if (k == 1u) {
        LDR_IMG(WRITING, LDR_SAY_Y, LA_R_INK);
        LDR_IMG(NOOFF, LDR_SUB_Y, LA_R_SUB);
    } else {
        LDR_IMG(FAILED, LDR_SAY_Y, LA_R_RED);
        LDR_IMG(AGAIN, LDR_SUB_Y, LA_R_SUB);
    }
}
static void ldr_percent(uint32_t p)                  /* "57%" under the logo, ranged right on it; 0xFFFF: none */
{
    uint32_t dg[4], n = 0, w = 0, x, i;
    lcd_fill(120, LDR_PCT_Y, 120, LA_DIG_H, LA_BG);  /* (its right half only: the version stays on the left) */
    if (p > 100u)
        return;
    if (p >= 100u)
        dg[n++] = 1u;
    if (p >= 10u)
        dg[n++] = p / 10u % 10u;
    dg[n++] = p % 10u;
    dg[n++] = 10u;                                  /* (%) */
    for (i = 0; i + 1u < n; i++)
        w += LA_DIG_W[dg[i]];                       /* (the digits before the %: the number grows to the left) */
    for (x = (240u - LA_LOGO_W) / 2u + LA_LOGO_INK_R - LA_PCT_INK_R - w, i = 0; i < n; x += LA_DIG_W[dg[i]], i++)
        ldr_blit(x, LDR_PCT_Y, LA_DIG_W[dg[i]], LA_DIG_H, LA_DIG[dg[i]], LA_R_INK);
}
static void ldr_screen(void)
{
    ldr_halo_make();
    lcd_init();                                     /* (the panel cleared, on) */
    lcd_fill(0, 0, 240, 240, LA_BG);
    ldr_logo();
    ldr_say(0);
    LDR_IMG(SITE, LDR_SITE_Y, LA_R_SUB);
    ldr_blit((240u - LA_LOGO_W) / 2u + LA_LOGO_INK_L, LDR_PCT_Y + LA_DIG_H - LA_VER_H, LA_VER_W, LA_VER_H, LA_VER,
             LA_R_SUB);                             /* the version it installs, under the logo on the left (Marc, 15/11) */
    lcd_sync();
}
static void ldr_anim(uint32_t ms)                   /* while it waits: a slanted glint runs through the logo, then rests */
{
    if (!ldr_idle || (int32_t)(ms - ldr_next) < 0)
        return;
    ldr_gx += 6;
    ldr_next = ms + 30u;                            /* (6 px every 30 ms: across in 1.5 s) */
    if (ldr_gx > (int32_t)LA_LOGO_W + LDR_GLINT) {
        ldr_gx = LDR_GX0;
        ldr_next = ms + 900u;                       /* (a rest, the logo plain) */
    }
    ldr_logo();
    lcd_sync();
}
static void ldr_bar(uint32_t done, uint32_t total)
{
    uint32_t n = done * LA_LOGO_W / total;          /* (the app area * 225: below 2^32) */
    uint32_t p = done * 100u / total;               /* (the app area * 100: below 2^32) */
    if (n > LA_LOGO_W)
        n = LA_LOGO_W;
    if (!ldr_writing || n < ldr_fill) {             /* a write starts (again) */
        ldr_idle = 0;
        ldr_say(1);
        ldr_fill = n;
        ldr_writing = 1;
        ldr_gx = LDR_GX0;
        ldr_logo();
        ldr_percent(ldr_pct = 0);
    }
    if (n != ldr_fill) {                            /* (the logo only when its fill moves: 225 steps at most) */
        ldr_fill = n;
        ldr_logo();
    }
    if (p > 100u)
        p = 100u;
    if (p != ldr_pct)                               /* (the number only when it changes) */
        ldr_percent(ldr_pct = p);
    lcd_sync();
}
/* written, before the restart: one last glint over the whole logo, cream (LDR_WAIT: loader.c's wait, which feeds the
 * watchdog; none in the host test) */
#ifndef LDR_WAIT
#define LDR_WAIT(ms) ((void)0)
#endif
static void ldr_done(void)
{
    ldr_fill = LA_LOGO_W;
    ldr_writing = 0;
    for (ldr_gx = LDR_GX0 + 8; ldr_gx <= (int32_t)LA_LOGO_W + LDR_GLINT; ldr_gx += 8) {
        ldr_logo();
        lcd_sync();
        LDR_WAIT(16);
    }
    ldr_gx = LDR_GX0;
    ldr_logo();
    lcd_sync();
}
static void ldr_failed(void)                        /* a session that wrote nothing or stopped: the way out */
{
    ldr_say(2);
    ldr_idle = 0;
    ldr_fill = 0;
    ldr_logo();
    ldr_percent(ldr_pct = 0xFFFFu);
    lcd_sync();
    ldr_writing = 0;
}
