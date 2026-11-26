/* SPDX-License-Identifier: GPL-3.0-only
 * Copyright (C) 2026 illuminus5 (Skiff's test), zvenson */
/* Host test of the update loader's screen (firmware/loader/ldr_screen.c) through src/lcd.c, on a fake ST7789: the
 * window and RAMWR commands into a 240 x 240 frame. UPDATE MODE after boot: the logo (ldr_art.h) dark off-white, the
 * status, what to do, guru-600.com; the glint running through the logo; WRITING at 50 %: the logo cream on its left half,
 * "50%" under it, ranged right; a second write starting over; UPDATE FAILED in red; only the screen's colours, nothing
 * outside the panel.
 * With a DIR, the screens as PPM files.   tests/ldr_screen_test [DIR] */
#include <stdint.h>
#include <stdio.h>
#include <string.h>

static uint16_t fb[240][240];                   /* RGB565 as the panel stores it */
static uint32_t win[4], cx, cy, cmd, outside;
static const uint8_t *pend;
static uint32_t pend_n;
static void fm1_lcd_hw_init(void) {}
static void fm1_lcd_baud(uint32_t b) { (void)b; }
static void fm1_lcd_backlight(uint32_t on) { (void)on; }
static void fm1_lcd_deselect(void) {}
static void fm1_lcd_send_cmd(uint8_t c)
{
    cmd = c;
    if (c == 0x2C) {
        cx = win[0];
        cy = win[2];
    }
}
static void fm1_lcd_send_data(const void *p, uint32_t n) { pend = p, pend_n = n; }
static void fm1_lcd_wait(void)                  /* the DMA's bytes land here, as the panel takes them */
{
    uint32_t i;
    if (!pend_n)
        return;                                 /* (a command's own byte) */
    if (cmd == 0x2A || cmd == 0x2B)
        for (i = 0; i < 2u; i++)
            win[(cmd == 0x2B) * 2u + i] = (uint32_t)pend[2u * i] << 8 | pend[2u * i + 1u];
    else if (cmd == 0x2C)
        for (i = 0; i + 1u < pend_n; i += 2u) {
            if (cx > 239u || cy > 239u || win[1] > 239u || win[3] > 239u)
                outside++;
            else
                fb[cy][cx] = (uint16_t)(pend[i] << 8 | pend[i + 1u]);
            if (++cx > win[1]) {
                cx = win[0];
                cy++;
            }
        }
    pend_n = 0;
}
#define fm1_irq_off() ((void)0)
#define fm1_irq_on() ((void)0)
#include "../firmware/src/lcd.c"
#include "../firmware/loader/ldr_art.h"
#include "../firmware/src/guru_version.h"
#include "../firmware/loader/ldr_screen.c"

static int bad;
static void check(const char *what, int ok)
{
    printf("ldr_screen: %-86s %s\n", what, ok ? "ok" : "FAIL");
    bad += !ok;
}
static uint32_t count(uint32_t x0, uint32_t y0, uint32_t x1, uint32_t y1, uint16_t c)   /* pixels of colour c */
{
    uint32_t x, y, n = 0;
    for (y = y0; y < y1; y++)
        for (x = x0; x < x1; x++)
            n += fb[y][x] == c;
    return n;
}
static void ppm(const char *dir, const char *name)
{
    char path[512];
    FILE *f;
    uint32_t x, y;
    if (!dir)
        return;
    snprintf(path, sizeof path, "%s/%s.ppm", dir, name);
    if (!(f = fopen(path, "wb")))
        return;
    fprintf(f, "P6 240 240 255\n");
    for (y = 0; y < 240u; y++)
        for (x = 0; x < 240u; x++) {
            uint16_t v = fb[y][x];
            fputc((v >> 11) * 255 / 31, f), fputc((v >> 5 & 63) * 255 / 63, f), fputc((v & 31) * 255 / 31, f);
        }
    fclose(f);
}

#define SW(v) ((uint16_t)((v) >> 8 | (v) << 8))         /* a ramp's colour as the panel stores it */
static int in_ramp(uint16_t c, const uint16_t *r)
{
    uint32_t k;
    for (k = 0; k < 16u; k++)
        if (c == SW(r[k]))
            return 1;
    return 0;
}
#define LX ((240u - LA_LOGO_W) / 2u)
static int palette_only(void)                        /* only the ramps' colours (in the logo's box: the glow too) */
{
    uint32_t x, y;
    for (y = 0; y < 240u; y++)
        for (x = 0; x < 240u; x++) {
            uint16_t c = fb[y][x];
            if (y >= LDR_LOGO_Y && y < LDR_LOGO_Y + LA_LOGO_H && x >= LX && x < LX + LA_LOGO_W)
                continue;
            if (!in_ramp(c, LA_R_DIM) && !in_ramp(c, LA_R_FULL) && !in_ramp(c, LA_R_INK) && !in_ramp(c, LA_R_SUB) &&
                !in_ramp(c, LA_R_RED))
                return 0;
        }
    return 1;
}
static int lit(uint32_t x, uint32_t y)               /* a logo pixel the glint or the glow lights */
{
    uint16_t c = fb[LDR_LOGO_Y + y][LX + x];
    return !in_ramp(c, LA_R_DIM) && !in_ramp(c, LA_R_FULL);
}
static uint32_t logo(uint32_t x0, uint32_t x1, uint16_t c)   /* the logo's pixels of colour c, its columns [x0, x1) */
{
    return count(LX + x0, LDR_LOGO_Y, LX + x1, LDR_LOGO_Y + LA_LOGO_H, c);
}
static uint32_t filled_to(void)                      /* the first logo column after the cream: the fill */
{
    uint32_t x, y, last = 0;
    for (x = 0; x < LA_LOGO_W; x++)
        for (y = 0; y < LA_LOGO_H; y++)
            if (fb[LDR_LOGO_Y + y][LX + x] == SW(LA_R_FULL[15]))
                last = x + 1u;
    return last;
}
static uint32_t glint_at(void)                       /* the first lit column, or 999 */
{
    uint32_t x, y;
    for (x = 0; x < LA_LOGO_W; x++)
        for (y = 0; y < LA_LOGO_H; y++)
            if (lit(x, y))
                return x;
    return 999u;
}
static uint32_t lit_rows(uint32_t x0, uint32_t x1)   /* rows with a lit pixel in columns [x0, x1) */
{
    uint32_t x, y, n = 0, any;
    for (y = 0; y < LA_LOGO_H; y++) {
        for (any = 0, x = x0; x < x1; x++)
            any |= lit(x, y);
        n += any;
    }
    return n;
}
static uint32_t lit_left(uint32_t y)                 /* a row's first lit column, or 999 */
{
    uint32_t x;
    for (x = 0; x < LA_LOGO_W; x++)
        if (lit(x, y))
            return x;
    return 999u;
}
static uint32_t ink_from(uint32_t x0, uint32_t y0, uint32_t y1, const uint16_t *r)   /* pixels at least half the colour
                                                                                        * of ramp r, [x0, 240) x [y0, y1) */
{
    uint32_t n = 0, k;
    for (k = 8; k < 16u; k++)
        n += count(x0, y0, 240, y1, SW(r[k]));
    return n;
}
#define ink(y0, y1, r) ink_from(0, (y0), (y1), (r))
#define pct_ink() ink_from(120, LDR_PCT_Y, LDR_PCT_Y + LA_DIG_H, LA_R_INK)   /* (the percent: right of the version) */
#define ver_ink() (count(LX, LDR_PCT_Y, LX + 60u, LDR_PCT_Y + LA_DIG_H, SW(LA_R_SUB[15])) + \
                   count(LX, LDR_PCT_Y, LX + 60u, LDR_PCT_Y + LA_DIG_H, SW(LA_R_SUB[12])))   /* (the version's grey) */

int main(int argc, char **argv)
{
    const char *dir = argc > 1 ? argv[1] : NULL;
    uint32_t total = 0x93000u - 0x4000u, ms, g, moves = 0, rests = 0, last = 0, f, slant = 0, v0 = 0;   /* the app area, as ldr_core.c says */
    ldr_screen();
    ppm(dir, "ldr_update_mode");
    check("UPDATE MODE: the logo all dark off-white (none filled), no percent, the status, what to do, guru-600.com",
          logo(0, LA_LOGO_W, SW(LA_R_DIM[15])) > 1000u && logo(0, LA_LOGO_W, SW(LA_R_FULL[15])) == 0u &&
          pct_ink() == 0u && ink(LDR_SAY_Y, LDR_SAY_Y + LA_MODE_H, LA_R_INK) > 100u &&
          ink(LDR_SUB_Y, LDR_SUB_Y + LA_WAIT_H, LA_R_SUB) > 50u && ink(LDR_SITE_Y, LDR_SITE_Y + LA_SITE_H, LA_R_SUB) > 30u);
    check("the version under the logo, on the left: the firmware's own (guru_version.h; else run p600/make_ldr_screen.py)",
          !strcmp(LA_VERSION, GURU_VERSION) && ver_ink() > 10u);   /* (1.4.1: 19 px, its thin 1s; 1.4.0: 37) */
    v0 = ver_ink();
    check("only the screen's colours, the background everywhere else", palette_only() && count(0, 0, 240, 10, SW(LA_R_DIM[0])) == 2400u);
    for (ms = 0; ms < 20000u; ms += 10u) {           /* 20 s: the glint crosses the logo left to right, rests, again */
        ldr_anim(ms);
        g = glint_at();
        if (g != 999u && g > last)
            moves++;
        if (g == 999u && last != 999u)
            rests++;
        last = g;
        if (ms == 600u) {
            ppm(dir, "ldr_waiting");
            slant = lit_left(36u) + 6u < lit_left(14u) && lit_left(14u) != 999u;   /* (the bottom further left) */
        }
    }
    check("the glint: slanted, with its glow, across the logo left to right again and again, a rest between, nothing filled",
          moves > 100u && rests >= 6u && slant && filled_to() == 0u);
    ldr_bar(total / 2u, total);
    ppm(dir, "ldr_writing");
    f = filled_to();
    check("WRITING at 50 %: the logo cream on its left half, dark off-white on the right, \"50%\" under it, a glow at its edge only",
          f > LA_LOGO_W / 2u - 10u && f <= LA_LOGO_W / 2u + 1u && logo(LA_LOGO_W / 2u + 2u, LA_LOGO_W, SW(LA_R_DIM[15])) > 300u &&
          pct_ink() > 100u && lit_rows(LA_LOGO_W / 2u - 7u, LA_LOGO_W / 2u) > 5u &&
          glint_at() >= LA_LOGO_W / 2u - 7u && !ldr_idle);
    check("the version still there while it writes", ver_ink() == v0);
    ldr_anim(99999u);
    check("no glint once it writes", glint_at() >= LA_LOGO_W / 2u - 7u && filled_to() == f);
    ldr_bar(total, total);
    check("done: the whole logo cream, 100%, no glow", logo(0, LA_LOGO_W, SW(LA_R_DIM[15])) == 0u && ldr_pct == 100u &&
          glint_at() == 999u);
    ldr_done();
    check("written: one last glint, then the logo cream and plain", logo(0, LA_LOGO_W, SW(LA_R_DIM[15])) == 0u &&
          glint_at() == 999u && filled_to() > LA_LOGO_W - 8u);
    ldr_writing = 1;                                 /* (as after a session the host starts again) */
    ldr_bar(total / 4u, total);
    f = filled_to();
    check("a second write starts over (25 %: a quarter of the logo)", f > LA_LOGO_W / 4u - 10u && f <= LA_LOGO_W / 4u + 1u);
    ldr_failed();
    ppm(dir, "ldr_failed");
    check("UPDATE FAILED in red: the logo dark again, no percent, the way out",
          filled_to() == 0u && pct_ink() == 0u &&
          ink(LDR_SAY_Y, LDR_SAY_Y + LA_FAILED_H, LA_R_RED) > 100u && ink(LDR_SUB_Y, LDR_SUB_Y + LA_AGAIN_H, LA_R_SUB) > 30u);
    check("the version still there after a failure", ver_ink() == v0);
    check("nothing outside the panel, only the screen's colours", !outside && palette_only());
    printf("%s\n", bad ? "LDR SCREEN TEST FAILED" : "ldr_screen test passed");
    return bad != 0;
}
