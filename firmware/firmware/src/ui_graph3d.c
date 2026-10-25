/* SPDX-License-Identifier: GPL-3.0-only */
/* Guru-600: the panel's curves in 3D (MENU > DISPLAY > 3D; OFF: Felucca's flat ones). Drawn from the sound itself:
 * fx.c / audio.c keep the output's left and right channels (scope_buf, scope_buf_r: 512 samples at 22 kHz); each
 * frame g3_analyse takes them: the level (auto-scaled), the attacks, the stereo width, three spectra (mid, left,
 * right: 48 bands 43 Hz .. 11 kHz) and their histories. Besides: the notes the selected track plays (its voices), its
 * reverb send (P_REV), its LFO, its CUTOFF and RESONANCE.
 *   HOME    one style (MENU > DISPLAY > 3D): DISC (the default), WALLS, TUNNEL, CELL, WAVES, SPARKS, FLOWER; AUTO in turn
 *   ENV     the real envelope: the level of the last 4 s in relief, an orb of light at the present
 *   FLT ENV a plate of 32 x 32 columns: the spectrum spreading from the middle (now) to the edges (the past)
 *   LFO     a ring whose thickness is the track's LFO wave, turning, glowing
 *   FILTER  the spectrum as a surface to the horizon, lava below the cutoff, ice above, a slab of light at the cutoff
 * Integer only (no FPU): Q16 fixed point for the geometry (q16), Q8 pixels for the lines (anti-aliased), RGB565. The
 * mock-ups they follow: p600/maquettes/mock3d_v2.py */
typedef int32_t q16;                                  /* Q16 */
#define FXC(x) ((q16)((x) * 65536.0))
static __attribute__((noinline)) q16 fmul(q16 a, q16 b) { return (q16)(((int64_t)a * b) >> 16); }
/* n / d with 32-bit divisions only (the toolchain has no 64-bit one): both brought down until n fits */
static __attribute__((noinline)) int32_t g3_sdiv(int64_t n, int32_t d)
{
    uint64_t un = (uint64_t)(n < 0 ? -n : n);
    uint32_t ud = (uint32_t)(d < 0 ? -d : d), q;
    int neg = (n < 0) != (d < 0);
    while (un >> 31) {
        un >>= 1;
        ud >>= 1;
    }
    if (!ud)
        return neg ? -0x7FFFFFFF : 0x7FFFFFFF;
    q = (uint32_t)un / ud;
    return neg ? -(int32_t)q : (int32_t)q;
}
static q16 fdiv(q16 a, q16 b)                         /* (32-bit divisions when the values allow: the common case) */
{
    uint32_t ua = (uint32_t)(a < 0 ? -a : a), ub = (uint32_t)(b < 0 ? -b : b), q;
    if (!b)
        return 0;
    if (ua < 32768u)
        q = (ua << 16) / ub;
    else if (ua < (1u << 23) && ub >= 256u)
        q = (ua << 8) / (ub >> 8);
    else
        return g3_sdiv((int64_t)a << 16, b);
    return (a < 0) != (b < 0) ? -(q16)q : (q16)q;
}
#define TURN(r) ((uint32_t)(int32_t)((int64_t)(r) * 10430))   /* radians (Q16) -> a phase (2^32 a turn) */
static inline q16 fsin(uint32_t ph) { return sine_i(ph) * 2; }
static inline q16 fcos(uint32_t ph) { return sine_i(ph + 0x40000000u) * 2; }

enum { G3_NONE, G3_HOME, G3_ENV, G3_FENV, G3_LFO, G3_FLT, G3_TRACKS };
enum { G3S_DISC, G3S_WALLS, G3S_TUNNEL, G3S_CELL, G3S_WAVES, G3S_SPARKS, G3S_FLOWER, G3S_BLOCKS, G3S_CASCADE, G3S_RIBBON, G3S_HELIX, G3S_N };
#ifdef FELUCCA_TEST_NO3D
static __attribute__((minsize)) int g3_on(void) { return 0; }   /* (tests: Felucca's flat panels) */
#else
static __attribute__((minsize)) int g3_on(void) { return 1; }
#endif   /* (always: MENU > DISPLAY > 3D is gone; ui_prefs3 unused) */
/* the style a page shows: HOME the DISC; the pages that had only the flat scope, each the style that says what it sets
 * (REVERB the cell and its glow, CHORUS the stereo walls, DLY the tunnel's echoing rings, ARP 2 a burst a note, ENV
 * DEST the pile of waves, CLOCK the flower, ARP the blocks); 0xFF none */
static uint32_t g3_pstyle = G3S_DISC;
static __attribute__((minsize)) uint32_t g3_page_style(const page_t *pg)
{
    static const struct { const char *t; uint8_t s; } M[] = {
        {"REVERB", G3S_CELL}, {"CHORUS", G3S_WALLS}, {"DLY", G3S_TUNNEL}, {"ARP 2", G3S_SPARKS}, {"ENV DEST", G3S_WAVES},
        {"CLOCK", G3S_FLOWER}, {"ARP", G3S_BLOCKS}, {"OSC 2", G3S_CASCADE}, {"POLY MOD", G3S_RIBBON}, {"LFO 2", G3S_HELIX},
    };
    uint32_t i;
    for (i = 0; i < NELEM(M); i++)
        if (str_eq(pg->title, M[i].t))
            return M[i].s;
    return 0xFFu;
}
static __attribute__((minsize)) uint32_t g3_style(void) { return g3_pstyle; }
static __attribute__((minsize)) uint32_t g3_kind(void)
{
    const page_t *pg = cur_page();
    if (!g3_on() || large_kind() == LK_TALL)
        return G3_NONE;
    if (ui.home) {
        g3_pstyle = G3S_DISC;
        return home_tracks() ? G3_NONE : G3_HOME;
    }
    if (g3_page_style(pg) != 0xFFu) {
        g3_pstyle = g3_page_style(pg);
        return G3_HOME;
    }
    if (TSEL->eng_req % NENGINES == ENGI_P600) {       /* the P600's OSCILLATORS (the engine's EDIT 1): as OSC 2; its MIXER
                                                        * page: the four tracks (Felucca's HOME TRACKS) */
        if (str_eq(pg->title, "EDIT 1")) {
            g3_pstyle = G3S_CASCADE;
            return G3_HOME;
        }
        if (pg->eng == ENGI_P600 + 1u && str_eq(pg->title, "MIXER"))
            return G3_TRACKS;
    }
    if (pg->graph == GR_ADSR)
        return str_eq(pg->title, "FLT ENV") ? G3_FENV : G3_ENV;
    if (pg->graph == GR_LFO)
        return G3_LFO;
    if (TSEL->eng_req % NENGINES == ENGI_P600 && pg->eng == ENGI_P600 + 1u && str_eq(pg->title, "FILTER"))
        return G3_FLT;
    return G3_NONE;
}

/* ------------------------------------------------------------------------------------------------- math --- */
static __attribute__((minsize)) uint32_t g3_isqrt(uint32_t v)
{
    uint32_t r = 0, b = 1u << 30;
    while (b > v)
        b >>= 2;
    while (b) {
        if (v >= r + b) {
            v -= r + b;
            r = (r >> 1) + b;
        } else {
            r >>= 1;
        }
        b >>= 2;
    }
    return r;
}
static __attribute__((minsize)) q16 fhypot(q16 x, q16 y)                          /* sqrt(x^2 + y^2), Q16 */
{
    uint64_t s = (uint64_t)((int64_t)x * x) + (uint64_t)((int64_t)y * y);
    uint32_t sh = 0;
    while (s > 0xFFFFFFFFull) {
        s >>= 2;
        sh++;
    }
    return (q16)(g3_isqrt((uint32_t)s) << sh);
}
static __attribute__((minsize)) q16 fexp2(q16 x)                                 /* 2^x, Q16 (x <= 14) */
{
    int32_t n = x >> 16;
    q16 f = x - (n << 16);
    q16 m = 65536 + fmul(f, FXC(0.6565) + fmul(FXC(0.3435), f));
    if (n < -30)
        return 0;
    return n >= 0 ? m << n : m >> -n;
}
static __attribute__((minsize)) q16 fexp(q16 x) { return fexp2(fmul(x, FXC(1.442695))); }
static __attribute__((minsize)) q16 flog2(q16 a)                                 /* log2(a), Q16, a > 0 */
{
    int32_t e = 31;
    q16 m, f;
    if (a <= 0)
        return -(30 << 16);
    while (!((uint32_t)a >> e))
        e--;
    m = e >= 16 ? a >> (e - 16) : a << (16 - e);      /* 1 .. 2 */
    f = m - 65536;
    return ((e - 16) << 16) + fmul(f, FXC(1.4427) - fmul(FXC(0.4427), f));
}
static __attribute__((minsize)) q16 fpow(q16 a, q16 e) { return a <= 0 ? 0 : fexp2(fmul(e, flog2(a))); }
static __attribute__((minsize)) q16 fclamp(q16 v) { return v < 0 ? 0 : v > 65536 ? 65536 : v; }
/* atan2 as Python's math.atan2(y, x): the angle of (x, y) from +x toward +y, a phase (2^32 a turn) */
static __attribute__((minsize)) uint32_t g3_atan2(q16 y, q16 x)
{
    q16 ax = x < 0 ? -x : x, ay = y < 0 ? -y : y, r, t;
    if (!ax && !ay)
        return 0;
    r = ax > ay ? fdiv(ay, ax) : fdiv(ax, ay);
    t = fmul(r, FXC(0.785398)) - fmul(fmul(r, r - 65536), FXC(0.2447) + fmul(FXC(0.0663), r));
    if (ay > ax) t = FXC(1.570796) - t;
    if (x < 0) t = FXC(3.141593) - t;
    if (y < 0) t = -t;
    return TURN(t);
}
static uint32_t g3_seed = 2463534242u;
static q16 g3_dt = 65536;                             /* the time since the last frame, in the mock-ups' frames (25 a second) */
static __attribute__((minsize)) uint32_t g3_rnd(void)
{
    g3_seed ^= g3_seed << 13;
    g3_seed ^= g3_seed >> 17;
    g3_seed ^= g3_seed << 5;
    return g3_seed;
}
static __attribute__((minsize)) q16 g3_uni(q16 lo, q16 hi) { return lo + fmul(hi - lo, (q16)(g3_rnd() >> 16)); }
static __attribute__((minsize)) q16 g3_norm(q16 sd)                              /* ~ a normal draw (three uniforms) */
{
    q16 s = (q16)(g3_rnd() >> 16) + (q16)(g3_rnd() >> 16) + (q16)(g3_rnd() >> 16) - FXC(1.5);
    return fmul(s, fmul(sd, FXC(2.0)));
}

/* ----------------------------------------------------------------------------------------------- colour --- */
static __attribute__((minsize)) uint16_t g3_mix(uint16_t a, uint16_t b, int32_t k)   /* a -> b, k 0..256 */
{
    int32_t r = a >> 11, g = (a >> 5) & 63, l = a & 31;
    if (k <= 0) return a;
    if (k >= 256) return b;
    r += (((b >> 11) - r) * k) >> 8;
    g += ((((b >> 5) & 63) - g) * k) >> 8;
    l += (((b & 31) - l) * k) >> 8;
    return (uint16_t)(r << 11 | g << 5 | l);
}
static __attribute__((minsize)) uint16_t g3_dim(uint16_t c, q16 k) { return g3_mix(T_SURF, c, fclamp(k) >> 8); }   /* toward the panel */
typedef struct { uint16_t k; uint8_t r, g, b; } g3stop_t;   /* k 0..1000 */
static __attribute__((minsize)) uint16_t g3_ramp(const g3stop_t *s, uint32_t n, q16 k)
{
    int32_t kk = (int32_t)(((int64_t)fclamp(k) * 1000) >> 16);
    uint32_t i;
    for (i = 1; i < n; i++)
        if (kk <= s[i].k) {
            int32_t u = (kk - s[i - 1].k) * 256 / (s[i].k - s[i - 1].k);
            return RGB(s[i - 1].r + ((s[i].r - s[i - 1].r) * u >> 8), s[i - 1].g + ((s[i].g - s[i - 1].g) * u >> 8),
                       s[i - 1].b + ((s[i].b - s[i - 1].b) * u >> 8));
        }
    return RGB(s[n - 1].r, s[n - 1].g, s[n - 1].b);
}
static const g3stop_t G3_HOT[] = {{0, 60, 10, 20}, {350, 255, 80, 70}, {650, 244, 150, 56}, {850, 255, 228, 40}, {1000, 255, 250, 230}};
static const g3stop_t G3_LAVA[] = {{0, 50, 8, 12}, {300, 200, 40, 30}, {600, 255, 120, 30}, {850, 255, 220, 80}, {1000, 255, 250, 230}};
static const g3stop_t G3_ICE[] = {{0, 10, 18, 50}, {350, 30, 70, 170}, {700, 60, 170, 230}, {1000, 210, 245, 255}};
static const g3stop_t G3_AURORA[] = {{0, 40, 15, 70}, {350, 110, 50, 170}, {650, 40, 170, 160}, {850, 110, 235, 130}, {1000, 230, 255, 220}};
static const g3stop_t G3_COLDWARM[] = {{0, 40, 50, 230}, {250, 50, 140, 255}, {450, 80, 220, 240}, {650, 255, 225, 80},
                                       {820, 255, 140, 40}, {1000, 255, 50, 40}};
static __attribute__((minsize)) uint16_t g3_hsv(uint32_t h, q16 s, q16 v)        /* h a phase (a turn), s, v 0..1 */
{
    uint64_t h6 = (uint64_t)h * 6u;
    uint32_t sec = (uint32_t)(h6 >> 32);
    q16 f = (q16)((h6 & 0xFFFFFFFFu) >> 16);
    q16 p = fmul(v, 65536 - s), q = fmul(v, 65536 - fmul(s, f)), t = fmul(v, 65536 - fmul(s, 65536 - f));
    q16 r, g, b;
    switch (sec) {
    case 0: r = v; g = t; b = p; break;
    case 1: r = q; g = v; b = p; break;
    case 2: r = p; g = v; b = t; break;
    case 3: r = p; g = q; b = v; break;
    case 4: r = t; g = p; b = v; break;
    default: r = v; g = p; b = q; break;
    }
    r = fclamp(r) * 255 >> 16;
    g = fclamp(g) * 255 >> 16;
    b = fclamp(b) * 255 >> 16;
    return RGB(r, g, b);
}
static __attribute__((minsize)) uint16_t g3_wheel(uint32_t th, q16 v)           /* the colour wheel round the disc (th 0 at the back), lit by v */
{
    q16 s = FXC(0.85) - (v > FXC(0.75) ? fmul(FXC(2.0), v - FXC(0.75)) : 0);
    return g3_dim(g3_hsv(th, s, 65536), 65536);       /* (full light always: the height says the level) */
}
#define G3_RED RGB(255, 80, 70)
#define G3_ORANGE RGB(244, 150, 56)
#define G3_PINK RGB(250, 124, 196)
#define G3_CYAN RGB(80, 200, 232)
#define G3_VIOLET RGB(168, 132, 255)
#define G3_BLUE RGB(70, 110, 255)
#define G3_WHITE RGB(255, 255, 255)

/* the screens' work arrays: one at a time, one place (POOL) */
static union {
    struct { int32_t tx[2][120], ty[2][120]; } walls;
    struct { int32_t px[50], py[50], bx[50], by[50]; } waves;
    struct { int32_t lx[128], ly[128]; } env;
    struct { uint16_t order[32 * 32]; } plate;
    struct { int32_t rz[72]; q16 wv[72]; uint8_t ord[72]; } lfo;
    struct { int32_t sx[2][24], sy[2][24]; uint8_t rv[44][24]; } flt;
    struct { int16_t hor[240], top[240]; int8_t w[14][72]; } cas;
} g3w __attribute__((section(".pool")));
static uint8_t g3_clip;                               /* (CASCADE: a pixel only above the horizon, g3w.cas) */

/* --------------------------------------------------------------------------------------------- drawing --- */
static uint8_t g3_add;                                /* 1: lines and fills add their light (glows) */
static int32_t g3_alpha = 256;                        /* a multiplier of every coverage */
static __attribute__((minsize)) void g3_plot(int32_t x, int32_t y, uint16_t c, int32_t a)   /* a: the coverage, 0..256 */
{
    uint16_t *p, o;
    if ((uint32_t)x >= cv_w || (uint32_t)y >= cv_h || a <= 0)
        return;
    a = a * g3_alpha >> 8;
    if (a <= 0)
        return;
    if (g3_clip) {                                     /* (CASCADE: hidden below the nearer waves; the layer's top kept) */
        if (y >= g3w.cas.hor[x])
            return;
        if (a >= 128 && y < g3w.cas.top[x])
            g3w.cas.top[x] = (int16_t)y;
    }
    p = &cv_px[(uint32_t)y * cv_w + (uint32_t)x];
    o = swap16(*p);
    if (g3_add) {
        int32_t r = (o >> 11) + (((c >> 11) * a) >> 8), g = ((o >> 5) & 63) + ((((c >> 5) & 63) * a) >> 8),
                l = (o & 31) + (((c & 31) * a) >> 8);
        *p = swap16((uint16_t)((r > 31 ? 31 : r) << 11 | (g > 63 ? 63 : g) << 5 | (l > 31 ? 31 : l)));
    } else {
        *p = swap16(g3_mix(o, c, a > 256 ? 256 : a));
    }
}
/* a line (Q8 ends) w (Q8 px) wide, anti-aliased: per column (or row) the span across it, its edges in part */
static __attribute__((minsize)) void g3_line(int32_t x0, int32_t y0, int32_t x1, int32_t y1, int32_t w, uint16_t c)
{
    int32_t dx = x1 - x0, dy = y1 - y0, adx, ady, t, hw, i, i0, i1, sl, len;
    if ((x0 < -4096 && x1 < -4096) || (x0 > 65536 && x1 > 65536) || (y0 < -4096 && y1 < -4096) || (y0 > 36000 && y1 > 36000))
        return;
    adx = dx < 0 ? -dx : dx;
    ady = dy < 0 ? -dy : dy;
    len = (int32_t)g3_isqrt((uint32_t)((adx >> 4) * (adx >> 4) + (ady >> 4) * (ady >> 4))) << 4;
    if (adx >= ady) {
        if (!adx)
            return;
        if (dx < 0) {
            t = x0; x0 = x1; x1 = t;
            t = y0; y0 = y1; y1 = t;
            dy = -dy;
        }
        hw = w * (len > adx ? len : adx) / adx / 2;
        sl = (dy << 12) / adx;
        i0 = (x0 + 128) >> 8;
        i1 = (x1 + 128) >> 8;
        if (i0 < 0) i0 = 0;
        if (i1 > (int32_t)cv_w) i1 = (int32_t)cv_w;
        for (i = i0; i < i1; i++) {
            int32_t yc = y0 + (int32_t)(((int64_t)sl * ((i << 8) + 128 - x0)) >> 12), a = yc - hw, b = yc + hw, py;
            for (py = a >> 8; py <= b >> 8; py++) {
                int32_t lo = a > py << 8 ? a : py << 8, hi = b < (py + 1) << 8 ? b : (py + 1) << 8;
                g3_plot(i, py, c, hi - lo);
            }
        }
    } else {
        if (dy < 0) {
            t = x0; x0 = x1; x1 = t;
            t = y0; y0 = y1; y1 = t;
            dx = -dx;
        }
        hw = w * len / ady / 2;
        sl = (dx << 12) / ady;
        i0 = (y0 + 128) >> 8;
        i1 = (y1 + 128) >> 8;
        if (i0 < 0) i0 = 0;
        if (i1 > (int32_t)cv_h) i1 = (int32_t)cv_h;
        for (i = i0; i < i1; i++) {
            int32_t xc = x0 + (int32_t)(((int64_t)sl * ((i << 8) + 128 - y0)) >> 12), a = xc - hw, b = xc + hw, px;
            for (px = a >> 8; px <= b >> 8; px++) {
                int32_t lo = a > px << 8 ? a : px << 8, hi = b < (px + 1) << 8 ? b : (px + 1) << 8;
                g3_plot(px, i, c, hi - lo);
            }
        }
    }
}
/* a line and its glow: g (0..256) of light added round it (two widths), then the line itself */
static __attribute__((minsize)) void g3_gline(int32_t x0, int32_t y0, int32_t x1, int32_t y1, int32_t w, uint16_t c, int32_t g)
{
    if (g > 0) {
        uint8_t ad = g3_add;
        int32_t al = g3_alpha;
        g3_add = 1;
        g3_alpha = al * g * 3 >> 11;
        g3_line(x0, y0, x1, y1, w + 3 * 256, c);
        g3_add = ad;
        g3_alpha = al;
    }
    g3_line(x0, y0, x1, y1, w, c);
}
static __attribute__((minsize)) void g3_dot(int32_t x, int32_t y, int32_t r, uint16_t c)   /* a disc, Q8 centre and radius */
{
    int32_t px, py;
    for (py = (y - r - 128) >> 8; py <= (y + r + 128) >> 8; py++)
        for (px = (x - r - 128) >> 8; px <= (x + r + 128) >> 8; px++) {
            int32_t ex = (px << 8) + 128 - x, ey = (py << 8) + 128 - y;
            int32_t d = (int32_t)g3_isqrt((uint32_t)(ex * ex + ey * ey));
            g3_plot(px, py, c, r - d + 128);
        }
}
/* a convex polygon (Q8 points), filled: each pixel whose centre is inside; a its opacity (256: opaque) */
static __attribute__((minsize)) void g3_fill(const int32_t *xs, const int32_t *ys, uint32_t n, uint16_t c, int32_t a)
{
    int32_t ymin = ys[0], ymax = ys[0], y, i;
    uint16_t sc = swap16(c);
    for (i = 1; i < (int32_t)n; i++) {
        if (ys[i] < ymin) ymin = ys[i];
        if (ys[i] > ymax) ymax = ys[i];
    }
    ymin = (ymin - 128 + 255) >> 8;
    ymax = (ymax - 128) >> 8;
    if (ymin < 0) ymin = 0;
    if (ymax >= (int32_t)cv_h) ymax = (int32_t)cv_h - 1;
    for (y = ymin; y <= ymax; y++) {
        int32_t yy = (y << 8) + 128, xl = 0x7FFFFFFF, xr = -0x7FFFFFFF, x, x0, x1;
        for (i = 0; i < (int32_t)n; i++) {
            int32_t j = i + 1 == (int32_t)n ? 0 : i + 1, ya = ys[i], yb = ys[j];
            if ((ya <= yy && yb > yy) || (yb <= yy && ya > yy)) {
                int32_t xi = xs[i] + g3_sdiv((int64_t)(xs[j] - xs[i]) * (yy - ya), yb - ya);
                if (xi < xl) xl = xi;
                if (xi > xr) xr = xi;
            }
        }
        if (xl > xr)
            continue;
        x0 = (xl - 128 + 255) >> 8;
        x1 = (xr - 128) >> 8;
        if (x0 < 0) x0 = 0;
        if (x1 >= (int32_t)cv_w) x1 = (int32_t)cv_w - 1;
        if (a >= 256 && !g3_add && g3_alpha >= 256)
            for (x = x0; x <= x1; x++)
                cv_px[(uint32_t)y * cv_w + (uint32_t)x] = sc;
        else if (!g3_add && g3_alpha >= 256) {         /* (see-through: a blend, inline) */
            uint16_t *p = &cv_px[(uint32_t)y * cv_w + (uint32_t)x0];
            int32_t cr = (c >> 11) * a, cg = ((c >> 5) & 63) * a, cb = (c & 31) * a, na = 256 - a;
            for (x = x0; x <= x1; x++, p++) {
                uint16_t o = swap16(*p);
                *p = swap16((uint16_t)((((o >> 11) * na + cr) >> 8) << 11 | ((((o >> 5) & 63) * na + cg) >> 8) << 5 |
                                       (((o & 31) * na + cb) >> 8)));
            }
        } else
            for (x = x0; x <= x1; x++)
                g3_plot(x, y, c, a);
    }
}
static __attribute__((minsize)) void g3_quad(int32_t ax, int32_t ay, int32_t bx, int32_t by, int32_t cx, int32_t cy, int32_t dx, int32_t dy,
                    uint16_t c, int32_t a)
{
    int32_t xs[4] = {ax, bx, cx, dx}, ys[4] = {ay, by, cy, dy};
    g3_fill(xs, ys, 4, c, a);
}
static const uint8_t G3_EXP[65] = {255, 223, 195, 170, 149, 130, 114, 99, 87, 76, 66, 58, 51, 44, 39, 34, 30, 26, 23, 20, 17,
                                   15, 13, 12, 10, 9, 8, 7, 6, 5, 4, 4, 3, 3, 3, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0,
                                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};   /* 255 exp(-u), u = i / 7.5 */
/* a glow of light round (x, y) (Q8): k (0..256) * exp(-d^2 / 2 s^2), added, out to 3 s */
static __attribute__((minsize)) void g3_halo(int32_t x, int32_t y, int32_t s, uint16_t c, int32_t k)
{
    int32_t px, py, r = s * 3, s2 = (int32_t)(((int64_t)s * s) >> 8);
    uint8_t ad = g3_add;
    if (k <= 0 || s <= 0)
        return;
    if (s2 < 1)
        s2 = 1;
    g3_add = 1;
    for (py = (y - r) >> 8; py <= (y + r) >> 8; py++) {
        if ((uint32_t)py >= cv_h)
            continue;
        for (px = (x - r) >> 8; px <= (x + r) >> 8; px++) {
            int32_t ex = (px << 8) + 128 - x, ey = (py << 8) + 128 - y;
            int32_t d2 = (int32_t)(((int64_t)ex * ex + (int64_t)ey * ey) >> 8);
            uint32_t u = (uint32_t)d2 * 15u / (uint32_t)(4 * s2);   /* (d^2 / 2 s^2, in 1/7.5) */
            if ((uint32_t)px < cv_w && u < 64u)
                g3_plot(px, py, c, (G3_EXP[u] * k) >> 8);
        }
    }
    g3_add = ad;
}
/* (no title on the panel: the page's name is in the footer) */

/* the camera: above the scene; x right, y up, z away (Q16 units); the far climbs to the horizon hy (as mock3d_v2.py proj) */
typedef struct { q16 cx, hy, f, cam, h, ky; } g3pj_t;
static __attribute__((minsize)) void g3_pj(const g3pj_t *c, q16 x, q16 y, q16 z, int32_t *sx, int32_t *sy)   /* -> Q8 pixels */
{
    q16 d = c->cam + z, k;
    if (d < FXC(0.2)) d = FXC(0.2);
    k = fdiv(c->f, d);
    *sx = (c->cx + fmul(x, k)) >> 8;
    *sy = (c->hy + fmul(fmul(c->h - y, k), c->ky)) >> 8;
}

/* ---------------------------------------------------------------------------------------------- the sound --- */
#define G3_NB 48
#define G3_FFT 512u
#define G3_HL 128u                                    /* the level's history */
#define G3_HS 44u                                     /* the spectrum's (mid) */
#define G3_HC 32u                                     /* left / right */
static const uint8_t G3_BAND[G3_NB + 1] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
                                           23, 24, 25, 26, 27, 28, 29, 30, 31, 35, 39, 44, 50, 56, 63, 71, 79, 89, 100,
                                           113, 127, 142, 160, 180, 202, 227, 255};   /* FFT bins (43 Hz each) */
#define G3_HB 24                                      /* the histories' bands (pairs) */
static struct {
    int16_t l[SCOPE_N], r[SCOPE_N];                   /* the last 512 samples, left and right */
    int16_t re[G3_FFT], im[G3_FFT];
    uint8_t init;
    q16 lev, onset, side, cent;                         /* 0..1 */
    int32_t pk, opk, top[3];                           /* (the auto-scale; each spectrum's top, log2 Q8) */
    uint8_t spec[3][G3_NB];                            /* mid, left, right: 0..255 */
    uint8_t hl[G3_HL];                                 /* the histories (rings) */
    uint8_t hs[G3_HS][G3_HB];
    uint8_t hc[2][G3_HC][G3_HB];
    uint32_t n;                                        /* frames analysed */
    uint32_t trig;                                     /* a rising zero crossing of the mid */
    int32_t peak;                                      /* the window's peak (left or right) */
} g3a __attribute__((section(".pool")));
#define G3_HLV(i) g3a.hl[(g3a.n + G3_HL - 1u - (i)) % G3_HL]   /* (i frames ago) */
#define G3_HSV(i) g3a.hs[(g3a.n + G3_HS - 1u - (i)) % G3_HS]
#define G3_HCV(c, i) g3a.hc[c][(g3a.n + G3_HC - 1u - (i)) % G3_HC]
static __attribute__((minsize)) uint32_t g3_rev9(uint32_t i)                   /* i's 9 bits reversed */
{
    uint32_t r = 0, b;
    for (b = 0; b < 9u; b++)
        r |= ((i >> b) & 1u) << (8u - b);
    return r;
}
static __attribute__((minsize)) void g3_fft(void)                              /* re (im 0) in place, radix 2, halved each stage: no overflow */
{
    uint32_t len, i, j;
    for (i = 0; i < G3_FFT; i++) {
        uint32_t r = g3_rev9(i);
        if (r > i) {
            int16_t t = g3a.re[i];
            g3a.re[i] = g3a.re[r];
            g3a.re[r] = t;
        }
        g3a.im[i] = 0;
    }
    for (len = 2; len <= G3_FFT; len <<= 1)
        for (j = 0; j < len / 2u; j++) {
            uint32_t ph = j << (32u - (uint32_t)__builtin_ctz(len));
            int32_t wr = sine_i(ph + 0x40000000u), wi = -sine_i(ph);
            for (i = 0; i < G3_FFT; i += len) {
                int16_t *ar = &g3a.re[i + j], *ai = &g3a.im[i + j], *br = &g3a.re[i + j + len / 2u], *bi = &g3a.im[i + j + len / 2u];
                int32_t tr = (*br * wr - *bi * wi) >> 15, ti = (*br * wi + *bi * wr) >> 15;
                *br = (int16_t)((*ar - tr) >> 1);
                *bi = (int16_t)((*ai - ti) >> 1);
                *ar = (int16_t)((*ar + tr) >> 1);
                *ai = (int16_t)((*ai + ti) >> 1);
            }
        }
}
static __attribute__((minsize)) int32_t g3_log2q8(uint32_t v)                  /* log2(v), Q8 (v >= 1) */
{
    int32_t e = 31;
    if (!v) v = 1;
    while (e && !(v >> e))
        e--;
    v = e >= 8 ? v >> (e - 8) : v << (8 - e);
    return (e << 8) + (int32_t)(((v - 256u) * 362u - ((v - 256u) * (v - 256u) * 106u >> 8)) >> 8);
}
static __attribute__((minsize)) void g3_spectrum(uint32_t which, const int16_t *a, const int16_t *b)   /* (a + b) / 2, or a alone (b 0) */
{
    uint32_t i, k;
    int32_t db[G3_NB], top = 0;
    for (i = 0; i < G3_FFT; i++) {
        int32_t s = b ? (a[i] + b[i]) / 2 : a[i];
        g3a.re[i] = (int16_t)((s * ((32767 - sine_i((i << 23) + 0x40000000u)) >> 1)) >> 15);   /* (Hann) */
    }
    g3_fft();
    for (k = 0; k < G3_NB; k++) {                     /* the band's mean magnitude (max + min / 2 a bin), in log2 */
        uint32_t s = 0, n = 0;
        for (i = G3_BAND[k]; i < (uint32_t)G3_BAND[k + 1] || n == 0; i++, n++) {
            uint32_t x = (uint32_t)(g3a.re[i] < 0 ? -g3a.re[i] : g3a.re[i]), y = (uint32_t)(g3a.im[i] < 0 ? -g3a.im[i] : g3a.im[i]);
            s += x > y ? x + y / 2u : y + x / 2u;
        }
        db[k] = g3_log2q8((s << 8) / n + 1u);
        if (db[k] > top)
            top = db[k];
    }
    if (top > g3a.top[which])                          /* (the top: the loudest lately, falling back slowly) */
        g3a.top[which] = top;
    else
        g3a.top[which] -= 1;
    if (g3a.top[which] < 9 * 256)
        g3a.top[which] = 9 * 256;
    for (k = 0; k < G3_NB; k++) {                     /* 72 dB below the top .. 6 dB below: 0 .. 255 */
        int32_t v = (db[k] - g3a.top[which] + 3062) * 255 / 2806;
        g3a.spec[which][k] = (uint8_t)(v < 0 ? 0 : v > 255 ? 255 : v);
    }
}
static __attribute__((minsize)) void g3_analyse(void)
{
    uint32_t w = scope_w, i;
    int64_t sm = 0, ss = 0;
    int32_t rms, rs, lr, pk = 1;
    q16 raw;
    if (!g3a.init) {
        g3a.pk = 300;
        g3a.opk = 2000;
        g3a.init = 1;
    }
    for (i = 0; i < SCOPE_N; i++) {
        int32_t l = scope_buf[(w + i) & (SCOPE_N - 1u)], r = scope_buf_r[(w + i) & (SCOPE_N - 1u)], m = (l + r) / 2, s = l - r;
        g3a.l[i] = (int16_t)l;
        g3a.r[i] = (int16_t)r;
        sm += (int64_t)m * m;
        ss += (int64_t)s * s;
        if (l > pk) pk = l; else if (-l > pk) pk = -l;
        if (r > pk) pk = r; else if (-r > pk) pk = -r;
    }
    g3a.peak = pk;
    rms = (int32_t)g3_isqrt((uint32_t)(sm / SCOPE_N));
    rs = (int32_t)g3_isqrt((uint32_t)(ss / SCOPE_N));
    if (rms > g3a.pk) g3a.pk = rms;                    /* (the auto-scale: the loudest lately) */
    else g3a.pk -= g3a.pk / 400 + 1;
    if (g3a.pk < 300) g3a.pk = 300;
    raw = rms < 40 ? 0 : g3_sdiv((int64_t)rms << 16, g3a.pk);   /* (silence: 0) */
    if (raw > 65536) raw = 65536;
    lr = raw - g3a.lev;                                /* the attack: the rise over the level */
    if (lr < 0) lr = 0;
    if (lr > g3a.opk) g3a.opk = lr;
    else g3a.opk -= g3a.opk / 200 + 1;
    if (g3a.opk < 2000) g3a.opk = 2000;
    g3a.onset = g3_sdiv((int64_t)lr << 16, g3a.opk);
    g3a.lev = raw > g3a.lev ? raw : (g3a.lev * 82 + raw * 18) / 100;
    g3a.side = rms ? fclamp(g3_sdiv((int64_t)rs << 16, 2 * rms)) : 0;
    for (i = 1; i + 240u < SCOPE_N; i++)               /* the trigger */
        if ((g3a.l[i - 1] + g3a.r[i - 1]) < 0 && (g3a.l[i] + g3a.r[i]) >= 0)
            break;
    g3a.trig = i + 240u < SCOPE_N ? i : 0;
    g3_spectrum(0, g3a.l, g3a.r);
    g3_spectrum(1, g3a.l, 0);
    g3_spectrum(2, g3a.r, 0);
    {
        int64_t a = 0, b = 0;
        for (i = 0; i < G3_NB; i++) {
            a += (int64_t)g3a.spec[0][i] * i;
            b += g3a.spec[0][i];
        }
        g3a.cent = b ? g3_sdiv(a << 16, (int32_t)(b * (G3_NB - 1))) : 0;
    }
    g3a.hl[g3a.n % G3_HL] = (uint8_t)(g3a.lev >> 8 > 255 ? 255 : g3a.lev >> 8);
    for (i = 0; i < G3_HB; i++) {
        g3a.hs[g3a.n % G3_HS][i] = (uint8_t)((g3a.spec[0][2 * i] + g3a.spec[0][2 * i + 1]) / 2);
        g3a.hc[0][g3a.n % G3_HC][i] = (uint8_t)((g3a.spec[1][2 * i] + g3a.spec[1][2 * i + 1]) / 2);
        g3a.hc[1][g3a.n % G3_HC][i] = (uint8_t)((g3a.spec[2][2 * i] + g3a.spec[2][2 * i + 1]) / 2);
    }
    g3a.n++;
}
static __attribute__((minsize)) q16 g3_mid(uint32_t i)                          /* the mid at sample i past the trigger, -1..1 of the peak */
{
    uint32_t k = g3a.trig + i;
    if (k >= SCOPE_N) k = SCOPE_N - 1u;
    return g3_sdiv((int64_t)(g3a.l[k] + g3a.r[k]) << 15, g3a.peak + 1);
}
static __attribute__((minsize)) q16 g3_chan(uint32_t c, uint32_t i)            /* the left (0) or right (1), -1..1 of the peak */
{
    uint32_t k = g3a.trig + i;
    if (k >= SCOPE_N) k = SCOPE_N - 1u;
    return g3_sdiv((int64_t)(c ? g3a.r[k] : g3a.l[k]) << 16, g3a.peak + 1);
}
/* the notes the track plays: its voices (held 1, ringing on after the key 0.5) */
typedef struct { uint8_t n; q16 w; } g3note_t;
static __attribute__((minsize)) uint32_t g3_notes(g3note_t *o)
{
    const track_t *t = TSEL;
    uint32_t i, k = 0;
    for (i = 0; i < NVOICE; i++)
        if (t->v[i].active) {
            o[k].n = t->v[i].note;
            o[k++].w = t->v[i].gate ? 65536 : 32768;
        }
    return k;
}

/* the particles (SPARKS, FLOWER's, FILTER's): one pool, one style at a time */
#define G3_NP 520u
typedef struct { int16_t x, y, vx, vy; uint16_t c; uint8_t life, a; } g3p_t;   /* 12 bytes: life Q8 (0: free), a the age
                                                   * (SPARKS, Q6) or the size (FLOWER); x y vx vy:
                                                   * Q16 >> g3_psh (the style's scale: SPARKS 4, the others 9) */
static uint32_t g3_psh = 4;
#define PX(p) ((q16)(p)->x << g3_psh)
#define PY(p) ((q16)(p)->y << g3_psh)
#define PVX(p) ((q16)(p)->vx << g3_psh)
#define PVY(p) ((q16)(p)->vy << g3_psh)
#define SX(p, v) ((p)->x = (int16_t)((v) >> g3_psh))
#define SY(p, v) ((p)->y = (int16_t)((v) >> g3_psh))
#define SVX(p, v) ((p)->vx = (int16_t)((v) >> g3_psh))
#define SVY(p, v) ((p)->vy = (int16_t)((v) >> g3_psh))
#define PAGE(p) ((q16)(p)->a << 10)
#define SAGE(p, v) ((p)->a = (uint8_t)((v) >> 10 > 255 ? 255 : (v) >> 10))
#define PLIFE(p) ((q16)(p)->life << 8)
#define SLIFE(p, v) ((p)->life = (uint8_t)((v) >> 8 > 255 ? 255 : (v) >> 8))
static g3p_t g3pt[G3_NP] __attribute__((section(".pool")));
static uint32_t g3_owner, g3_next;
static __attribute__((minsize)) g3p_t *g3_spawn(void)
{
    uint32_t i;
    for (i = 0; i < G3_NP; i++) {
        g3p_t *p = &g3pt[(g3_next + i) % G3_NP];
        if (!p->life) {
            g3_next = (g3_next + i + 1u) % G3_NP;
            return p;
        }
    }
    g3_next = (g3_next + 1u) % G3_NP;                  /* (full: one goes) */
    return &g3pt[g3_next];
}
static __attribute__((minsize)) void g3_own(uint32_t who)
{
    uint32_t i;
    g3_psh = who == 1u ? 4u : 9u;
    if (g3_owner != who) {
        for (i = 0; i < G3_NP; i++)
            g3pt[i].life = 0;
        g3_owner = who;
    }
}


/* ----------------------------------------------------------------------------------------------- HOME --- */
/* DISC: a disc in perspective, a bar standing per band round it, lows at the back, highs at the front; its left half
 * the left channel, its right half the right; the colour wheel round it; in the middle a glow toward the bars that rise */
static int16_t g3_dpk[2][G3_NB] __attribute__((section(".pool")));
static const g3pj_t G3_CDISC = {FXC(120), FXC(6), FXC(230), FXC(3.2), FXC(2.0), FXC(0.62)};
static __attribute__((minsize)) void g3_disc_pt(uint32_t th, q16 r, q16 y, int32_t *X, int32_t *Y)
{
    g3_pj(&G3_CDISC, fmul(fsin(th), fmul(r, FXC(1.25))), y, FXC(1.6) + fmul(fcos(th), fmul(r, FXC(1.15))), X, Y);
}
static __attribute__((minsize)) void g3s_disc(void)
{
    const q16 r0 = FXC(0.95), r1 = FXC(1.3), base = FXC(-0.5);
    const uint32_t da = 16106127u;                     /* (a bar: 0.36 of its 1/96 turn) */
    uint8_t circ[96];
    int32_t b, s, q, k;
    for (b = 0; b < G3_NB; b++) {
        circ[b] = g3a.spec[2][b];                      /* (round the circle: the right side 0 .. pi, then the left) */
        circ[95 - b] = g3a.spec[1][b];
        for (s = 0; s < 2; s++) {
            int32_t v = g3a.spec[1 + s][b] * 4;
            g3_dpk[s][b] = (int16_t)(v > g3_dpk[s][b] - 20 ? v : g3_dpk[s][b] - 20);
        }
    }
    for (k = 12; k >= 1; k--) {                        /* the glow, outer rings first: each way the wheel's colour */
        q16 rr = r0 * k / 12, fall = fpow(65536 - 65536 * k / 12, FXC(0.8));
        for (q = 0; q < 48; q++) {
            uint32_t u0 = (uint32_t)q * (0xFFFFFFFFu / 48u), u1 = u0 + 0xFFFFFFFFu / 48u, um = u0 + 0x7FFFFFFFu / 48u;
            int32_t e = 0, j, xs[3], ys[3];
            q16 inten;
            for (j = 2 * q - 5; j <= 2 * q + 6; j++)
                if (circ[(j + 96) % 96] > e) e = circ[(j + 96) % 96];
            inten = fmul(fmul(FXC(0.2) + fmul(FXC(0.5), g3a.lev), fall), FXC(0.4) + fmul(FXC(0.6), e * 257));
            g3_disc_pt(u0, 0, base, &xs[0], &ys[0]);
            g3_disc_pt(u0, rr, base, &xs[1], &ys[1]);
            g3_disc_pt(u1, rr, base, &xs[2], &ys[2]);
            g3_fill(xs, ys, 3, g3_dim(g3_wheel(um, 65536), FXC(0.1) + inten), 256);
        }
    }
    for (b = 0; b < G3_NB; b++)                        /* the bars, the back ones first */
        for (s = 0; s < 2; s++) {
            uint32_t th = (uint32_t)(2 * b + 1) * (0xFFFFFFFFu / 192u);
            q16 v = g3a.spec[1 + s][b] * 257, pk = g3_dpk[s][b] * 64, top = base + FXC(0.04) + fmul(v, FXC(1.3));
            q16 shade = FXC(0.6) + fmul(FXC(0.2), 65536 - fcos(th));
            int32_t x[6], y[6], px0, py0, px1, py1;
            q16 py = top + FXC(0.06) + fmul(pk > v ? pk - v : 0, FXC(1.3)), rm = (r0 + r1) / 2;
            uint16_t c;
            if (s == 0)
                th = 0u - th;                           /* (the left: the other way round) */
            c = g3_wheel(th, v);
            g3_disc_pt(th - da, r1, base, &x[0], &y[0]);
            g3_disc_pt(th + da, r1, base, &x[1], &y[1]);
            g3_disc_pt(th + da, r1, top, &x[2], &y[2]);
            g3_disc_pt(th - da, r1, top, &x[3], &y[3]);
            g3_quad(x[0], y[0], x[1], y[1], x[2], y[2], x[3], y[3], g3_dim(c, fmul(shade, FXC(0.8))), 256);
            g3_disc_pt(th + da, fmul(r0, FXC(1.04)), top, &x[4], &y[4]);
            g3_disc_pt(th - da, fmul(r0, FXC(1.04)), top, &x[5], &y[5]);
            g3_quad(x[3], y[3], x[2], y[2], x[4], y[4], x[5], y[5], g3_dim(c, shade), 256);
            g3_disc_pt(th - da, rm, py, &px0, &py0);
            g3_disc_pt(th + da, rm, py, &px1, &py1);
            g3_line(px0, py0, px1, py1, 256, g3_dim(G3_WHITE, FXC(0.25) + fmul(FXC(0.6), pk)));
        }
}

/* WALLS: two walls, each with its channel's wave: together in mono (one), apart in stereo (a corridor), the louder the
 * wider; they lie on the floor in silence; threads of light from crest to crest between them; the floor lit */
static const g3pj_t G3_CWALL = {FXC(120), FXC(20), FXC(170), FXC(3.2), FXC(1.9), FXC(0.62)};
static q16 g3w_cy, g3w_sy, g3w_turn;
static __attribute__((minsize)) void g3_wall_pt(q16 x, q16 y, q16 z, int32_t *X, int32_t *Y)
{
    g3_pj(&G3_CWALL, fmul(x, g3w_cy) + fmul(z - FXC(4), g3w_sy) + fmul(FXC(0.9), g3w_turn), y,
          -fmul(x, g3w_sy) + fmul(z - FXC(4), g3w_cy) + FXC(4), X, Y);
}
static __attribute__((minsize)) void g3s_walls(void)
{
    enum { N = 120 };
    int32_t (*tx)[N] = g3w.walls.tx, (*ty)[N] = g3w.walls.ty;
    q16 lv = g3a.lev, d, g, op;
    int32_t i, k, w, nw;
    uint32_t run = g3a.n % 100u;
    d = fmul(fmul(g3a.side, FXC(16)), FXC(0.25) + fmul(FXC(1.1), lv));
    if (d > FXC(2.4)) d = FXC(2.4);
    g3w_turn = fclamp(65536 - fdiv(d, FXC(0.8)));
    g3w_cy = fcos(TURN(fmul(FXC(0.42), g3w_turn)));
    g3w_sy = fsin(TURN(fmul(FXC(0.42), g3w_turn)));
    g = fmul(lv, FXC(1.3));
    op = fclamp(fdiv(d, FXC(1.2)));
    nw = d > FXC(0.05) ? 2 : 1;
    for (k = 0; k < 11; k++) {                         /* the floor */
        int32_t x0, y0, x1, y1;
        g3_wall_pt(FXC(0.5) * (k - 5), FXC(-1.0), 0, &x0, &y0);
        g3_wall_pt(FXC(0.5) * (k - 5), FXC(-1.0), FXC(9), &x1, &y1);
        g3_line(x0, y0, x1, y1, 256, RGB(40, 37, 34));
    }
    for (k = 0; k < 10; k++) {
        int32_t x0, y0, x1, y1;
        q16 z = fmul(FXC(0.9), FXC(1) * (k + 1) - (q16)(run * 655));
        g3_wall_pt(FXC(-2.5), FXC(-1.0), z, &x0, &y0);
        g3_wall_pt(FXC(2.5), FXC(-1.0), z, &x1, &y1);
        g3_line(x0, y0, x1, y1, 256, RGB(40, 37, 34));
    }
    if (nw == 2)                                       /* the corridor's floor, lit between the walls */
        for (i = 0; i < N - 1; i++) {
            int32_t x[4], y[4];
            q16 z0 = FXC(8) * i / N, z1 = FXC(8) * (i + 1) / N, kk = 65536 - 65536 * i / N;
            g3_wall_pt(-d, FXC(-1.0), z0, &x[0], &y[0]);
            g3_wall_pt(d, FXC(-1.0), z0, &x[1], &y[1]);
            g3_wall_pt(d, FXC(-1.0), z1, &x[2], &y[2]);
            g3_wall_pt(-d, FXC(-1.0), z1, &x[3], &y[3]);
            g3_fill(x, y, 4, g3_dim(RGB(90, 60, 120), fmul(fmul(fmul(FXC(0.35), op), kk), FXC(0.4) + fmul(FXC(0.6), lv))), 256);
        }
    for (w = 0; w < nw; w++) {                         /* the walls: the left (red) first, behind */
        q16 x = nw == 2 ? (w ? d : -d) : 0;
        uint16_t c = nw == 2 ? (w ? G3_CYAN : G3_RED) : G3_ORANGE;
        for (i = 0; i < N; i++) {
            uint32_t si = (uint32_t)i * 11u / 4u;
            q16 s = nw == 2 ? g3_chan((uint32_t)w, si) : g3_mid(si);
            g3_wall_pt(x, FXC(-1.0) + fmul(lv, FXC(1.9)) + fmul(s, g), FXC(8) * i / N, &tx[w][i], &ty[w][i]);
        }
        for (i = 0; i < N - 1; i++) {
            int32_t bx0, by0, bx1, by1;
            q16 kk = 65536 - 65536 * i / N;
            g3_wall_pt(x, FXC(-1.0), FXC(8) * i / N, &bx0, &by0);
            g3_wall_pt(x, FXC(-1.0), FXC(8) * (i + 1) / N, &bx1, &by1);
            g3_quad(tx[w][i], ty[w][i], tx[w][i + 1], ty[w][i + 1], bx1, by1, bx0, by0, g3_dim(c, FXC(0.10) + fmul(FXC(0.22), kk)), 256);
        }
        for (i = 0; i < N - 1; i++) {
            q16 kk = 65536 - 65536 * i / N;
            g3_gline(tx[w][i], ty[w][i], tx[w][i + 1], ty[w][i + 1], (int32_t)((FXC(0.8) + fmul(FXC(1.4), kk)) >> 8),
                     g3_dim(c, FXC(0.25) + fmul(FXC(0.75), kk)), 110);
        }
    }
    if (nw == 2)                                       /* the threads of light, crest to crest */
        for (i = 0; i < N - 1; i += 3) {
            uint32_t si = (uint32_t)i * 11u / 4u;
            q16 kk = 65536 - 65536 * i / N, diff = fclamp(fmul(g3_chan(0, si) - g3_chan(1, si), fmul(g, FXC(3))));
            q16 a = fmul(fmul(fmul(op, FXC(0.3) + fmul(FXC(0.7), kk)), FXC(0.55) + fmul(FXC(0.45), diff)), FXC(0.5) + fmul(FXC(0.5), lv));
            int32_t u, px = tx[0][i], py = ty[0][i];
            if (g3_chan(0, si) < g3_chan(1, si))
                diff = fclamp(fmul(g3_chan(1, si) - g3_chan(0, si), fmul(g, FXC(3))));
            for (u = 1; u <= 6; u++) {
                int32_t x = tx[0][i] + (tx[1][i] - tx[0][i]) * u / 6, y = ty[0][i] + (ty[1][i] - ty[0][i]) * u / 6;
                y -= (int32_t)(((int64_t)fmul(fsin((uint32_t)u * 0x15555555u), FXC(3) + fmul(FXC(10), diff)) * kk) >> 24);
                g3_line(px, py, x, y, 256, g3_dim(g3_mix(G3_RED, G3_CYAN, (u * 2 - 1) * 256 / 12), a));
                px = x;
                py = y;
            }
        }
}

/* TUNNEL: each waveform a ring, flying at us */
#define G3_TR 22u
#define G3_TP 60u
static struct { int8_t w[G3_TR][G3_TP]; uint8_t lv[G3_TR]; uint32_t n; } g3tun __attribute__((section(".pool")));
static __attribute__((minsize)) void g3s_tunnel(void)
{
    uint32_t j, i, slot = g3tun.n % G3_TR;
    uint32_t rot = g3a.n * 34172000u;                   /* (0.05 rad a frame) */
    for (i = 0; i < G3_TP; i++) {
        q16 m = g3_mid(i * 5u) >> 9;
        g3tun.w[slot][i] = (int8_t)(m > 127 ? 127 : m < -127 ? -127 : m);
    }
    g3tun.lv[slot] = (uint8_t)(g3a.lev >> 8 > 255 ? 255 : g3a.lev >> 8);
    g3tun.n++;
    for (j = 0; j < G3_TR; j++) {                       /* the oldest (far) first */
        uint32_t age = G3_TR - 1u - j, s;
        q16 z, k, dimk, wd;
        uint16_t c;
        int32_t px = 0, py = 0;
        if (age >= g3tun.n)
            continue;
        s = (g3tun.n - 1u - age) % G3_TR;
        z = FXC(0.15) + FXC(0.3) * (int32_t)age;
        k = fdiv(FXC(95), z + FXC(0.6));
        dimk = 65536 - 65536 * (int32_t)age / (int32_t)G3_TR;
        if (dimk < FXC(0.08)) dimk = FXC(0.08);
        wd = FXC(0.6) + fmul(FXC(1.6), age < 8u ? 65536 - 65536 * (int32_t)age / 8 : 0);
        c = g3_dim(g3_ramp(G3_HOT, 5, FXC(0.25) + fmul(FXC(0.75), g3tun.lv[s] * 257)), dimk);
        for (i = 0; i <= G3_TP; i++) {
            uint32_t a = (i % G3_TP) * (0xFFFFFFFFu / G3_TP) + rot;
            q16 r = FXC(0.75) + fmul(FXC(0.45), g3tun.w[s][i % G3_TP] * 516);
            int32_t x = (FXC(120) + fmul(fmul(r, fcos(a)), k)) >> 8, y = (FXC(61) + fmul(fmul(fmul(r, fsin(a)), FXC(0.9)), k)) >> 8;
            if (i)
                g3_gline(px, py, x, y, (int32_t)(wd >> 8), c, age < 7u ? 60 : 0);
            px = x;
            py = y;
        }
    }
}

/* CELL: a solid, round when the sound is dark, a cube when bright, spikes on the attacks; in stereo it divides in two
 * (a faint membrane while they part); its lines glow with the reverb (Tron): pink close, violet further, blue far */
static __attribute__((minsize)) void g3_cell_one(int32_t cx, q16 sharp, q16 spikes, q16 scale, uint32_t ry, q16 rx, q16 glow, int32_t blue)
{
    static q16 ct[25], st[25], cp[17], sp[17];
    q16 e = fdiv(FXC(2.0), 65536 + fmul(sharp, FXC(7)));
    q16 cry = fcos(ry), sry = fsin(ry), crx = fcos(TURN(rx)), srx = fsin(TURN(rx));
    uint32_t tph = fm1_ms * 1288490u;                   /* (t * 3 rad) */
    int32_t i, j, q, prevx = 0, prevy = 0;
#define SG(v) ((v) < 0 ? -fpow(-(v), e) : fpow((v), e))
    for (i = 0; i <= 24; i++) {
        uint32_t th = (uint32_t)i * (0xFFFFFFFFu / 24u);
        ct[i] = SG(fcos(th));
        st[i] = SG(fsin(th));
    }
    for (j = 0; j <= 16; j++) {
        uint32_t ph = 0xC0000000u + (uint32_t)j * 0x08000000u;   /* -pi/2 .. pi/2 */
        cp[j] = SG(fcos(ph));
        sp[j] = SG(fsin(ph));
    }
#undef SG
    for (i = 0; i < 12 + 7; i++) {                     /* 12 meridians (17 points), then 7 parallels (25) */
        int32_t np = i < 12 ? 17 : 25;
        for (q = 0; q < np; q++) {
            int32_t ti = i < 12 ? i * 2 : q, pj = i < 12 ? q : (i - 11) * 2, X, Y;
            uint32_t thp = (uint32_t)ti * (0xFFFFFFFFu / 24u), php = 0xC0000000u + (uint32_t)pj * 0x08000000u;
            q16 sv = fmul(fsin(thp * 6u + tph), fsin(php * 6u)), sk, x, y, z, xr, zr, yr, k;
            sk = 65536 + (sv > 0 ? fmul(fmul(spikes, FXC(0.35)), fmul(fmul(sv, sv), sv)) : 0);
            x = fmul(fmul(cp[pj], ct[ti]), sk);
            y = fmul(fmul(cp[pj], st[ti]), sk);
            z = fmul(sp[pj], sk);
            xr = fmul(x, cry) + fmul(z, sry);
            zr = -fmul(x, sry) + fmul(z, cry);
            yr = fmul(y, crx) - fmul(zr, srx);
            zr = fmul(y, srx) + fmul(zr, crx);
            k = fdiv(FXC(62), FXC(3) + fmul(zr, scale));
            X = (cx << 8) + (int32_t)(fmul(fmul(fmul(xr, scale), k), FXC(1.9)) >> 8);
            Y = (61 << 8) + (int32_t)(fmul(fmul(fmul(yr, scale), k), FXC(1.9)) >> 8);
            if (q) {
                if (!glow) {
                    g3_line(prevx, prevy, X, Y, 282, g3_dim(G3_PINK, FXC(0.35) + fmul(FXC(0.65), FXC(0.5) - zr / 2)));
                } else {                               /* the glow: three widths, three colours (added) */
                    g3_add = 1;
                    g3_alpha = (int32_t)(fmul(glow, FXC(0.30)) >> 8);
                    g3_line(prevx, prevy, X, Y, 256 * 3, G3_PINK);
                    g3_alpha = (int32_t)(fmul(glow, FXC(0.16)) >> 8);
                    g3_line(prevx, prevy, X, Y, 256 * 5, G3_VIOLET);
                    if (blue) {
                        g3_alpha = (int32_t)(fmul(glow, FXC(0.10)) >> 8);
                        g3_line(prevx, prevy, X, Y, 256 * 8, G3_BLUE);
                    }
                    g3_alpha = 256;
                    g3_add = 0;
                }
            }
            prevx = X;
            prevy = Y;
        }
    }
}
static __attribute__((minsize)) void g3s_cell(void)
{
    q16 lv = g3a.lev, sharp = fclamp(fmul(g3a.cent - FXC(0.25), FXC(2.4))), spikes = fclamp(fmul(g3a.onset, FXC(2.5)));
    q16 scale = FXC(0.75) + fmul(FXC(0.35), lv), sep = fclamp(fmul(fmul(g3a.side, FXC(7)), FXC(0.3) + lv)), R;
    q16 rev = TSEL->p[P_REV] * 516, tail = FXC(0.4) + fmul(FXC(0.6), fclamp(fmul(lv, FXC(1.5))));
    uint32_t ry = fm1_ms * 3006477u;                    /* (t * 0.7 rad) */
    q16 rx = FXC(0.45) + fmul(FXC(0.2), fsin(fm1_ms * 343597u));
    int32_t cx[2], nc, i;
    R = fmul(FXC(20.7 * 1.9), scale);
    nc = sep < FXC(0.04) ? 1 : 2;
    cx[0] = nc == 1 ? 120 : 120 - (int32_t)(fmul(sep, FXC(52)) >> 16);
    cx[1] = 120 + (int32_t)(fmul(sep, FXC(52)) >> 16);
    if (nc == 2 && sep < FXC(0.75)) {                  /* the membrane: round both, pinched, faint (a ray an angle) */
        int32_t px = 0, py = 0;
        uint16_t c = g3_dim(G3_PINK, fmul(FXC(0.32), 65536 - fdiv(sep, FXC(0.75))));
        q16 R2 = fmul(fmul(R, FXC(1.12)), fmul(R, FXC(1.12)));
        for (i = 0; i <= 64; i++) {
            uint32_t a = (uint32_t)i * (0xFFFFFFFFu / 64u);
            q16 ca = fcos(a), sa = fsin(a), lo = 0, hi = FXC(110), m = 0;
            int32_t it, x, y;
            for (it = 0; it < 14; it++) {              /* where the field of the two cells falls to 1 */
                q16 x0, y0, f = 0;
                int32_t c2;
                m = (lo + hi) / 2;
                x0 = fmul(m, ca);
                y0 = fmul(m, sa);
                for (c2 = 0; c2 < 2; c2++) {
                    q16 dx = x0 - ((cx[c2] - 120) << 16);
                    f += fdiv(R2, fmul(dx, dx) + fmul(y0, y0) + 65536);
                }
                if (f > 65536) lo = m; else hi = m;
            }
            x = (120 << 8) + (fmul(m, ca) >> 8);
            y = (61 << 8) + (fmul(m, sa) >> 8);
            if (i)
                g3_line(px, py, x, y, 256, c);
            px = x;
            py = y;
        }
    }
    if (rev > FXC(0.02))                               /* the glow under, then the lines */
        for (i = 0; i < nc; i++)
            g3_cell_one(cx[i], sharp, spikes, scale, ry + (uint32_t)i * 400000000u, rx,
                        fclamp(fmul(fmul(rev, FXC(2.0)), tail)), rev > FXC(0.4));
    for (i = 0; i < nc; i++)
        g3_cell_one(cx[i], sharp, spikes, scale, ry + (uint32_t)i * 400000000u, rx, 0, 0);
}

/* WAVES: the last waveforms piled up, past both sides, each filled with its colour at 20 %, the colour wheel by depth */
#define G3_WN 14u
#define G3_WP 50u
static struct { int8_t w[G3_WN][G3_WP]; uint8_t lv[G3_WN]; uint32_t n; } g3wav __attribute__((section(".pool")));
static __attribute__((minsize)) void g3s_waves(void)
{
    static const g3pj_t C = {FXC(120), FXC(6), FXC(200), FXC(3.2), FXC(2.1), FXC(0.62)};
    uint32_t j, i, slot = g3wav.n % G3_WN;
    uint32_t yaw = TURN(fmul(FXC(0.35), fsin(fm1_ms * 410154u)));   /* (sin(t * 0.6)) */
    q16 cyw = fcos(yaw), syw = fsin(yaw);
    for (i = 0; i < G3_WP; i++) {
        q16 m = g3_mid(i * 4u) >> 9;
        g3wav.w[slot][i] = (int8_t)(m > 127 ? 127 : m < -127 ? -127 : m);
    }
    g3wav.lv[slot] = (uint8_t)(g3a.lev >> 8 > 255 ? 255 : g3a.lev >> 8);
    g3wav.n++;
    for (j = G3_WN; j-- > 0;) {                         /* the far first */
        int32_t *px = g3w.waves.px, *py = g3w.waves.py, *bx = g3w.waves.bx, *by = g3w.waves.by;
        uint32_t s;
        q16 z = FXC(0.41) * (int32_t)j, k = 65536 - 65536 * (int32_t)j / (int32_t)G3_WN, kc, half, lk;
        uint16_t c, lc;
        if (j >= g3wav.n)
            continue;
        s = (g3wav.n - 1u - j) % G3_WN;
        kc = FXC(0.4) + fmul(FXC(0.6), g3wav.lv[s] * 257);
        c = g3_dim(g3_hsv((uint32_t)fmul(65536 * (int32_t)j / (int32_t)G3_WN, FXC(0.85)) << 16,
                          FXC(0.8) - (kc > FXC(0.8) ? fmul(FXC(2.0), kc - FXC(0.8)) : 0), 65536), FXC(0.35) + fmul(FXC(0.65), kc));
        half = fmul(fdiv(fmul(FXC(140), FXC(3.2) + z), FXC(200)), FXC(1.25));   /* (past both sides at any depth) */
        for (i = 0; i < G3_WP; i++) {
            q16 x = fmul(-65536 + 2 * 65536 * (int32_t)i / (int32_t)(G3_WP - 1), half);
            q16 X = fmul(x, cyw) + fmul(fmul(z, syw), FXC(0.3));
            g3_pj(&C, X, FXC(-0.2) + fmul(g3wav.w[s][i] * 516, FXC(1.5)), z, &px[i], &py[i]);
            g3_pj(&C, X, FXC(-1.4), z, &bx[i], &by[i]);
        }
        lk = FXC(0.2) + fmul(FXC(0.8), fpow(k, FXC(1.5)));
        lc = g3_dim(c, lk);
        if (j < 6u)                                    /* under the line: its colour at 20 % (the nearer ones) */
            for (i = 0; i + 1 < G3_WP; i++)
                g3_quad(px[i], py[i], px[i + 1], py[i + 1], bx[i + 1], by[i + 1], bx[i], by[i], lc, 51);
        for (i = 0; i + 1 < G3_WP; i++)
            g3_gline(px[i], py[i], px[i + 1], py[i + 1], j ? 205 : 461, lc, j < 4u ? 90 : 0);
    }
}

/* SPARKS: the keyboard bent into a circle (C1 at the bottom left, up the left, over the top, C7 at the bottom right): a
 * note played throws sparks from its side, slow for a low note, fast for a high one, blue .. red with its height */
static __attribute__((minsize)) void g3s_sparks(void)
{
    g3note_t nt[NVOICE];
    uint32_t nn = g3_notes(nt), i, n;
    q16 wsum = 0;
    g3_own(1);
    for (i = 0; i < nn; i++)
        wsum += nt[i].w;
    n = 0;                                             /* (few at a time: the pool holds 400, each must live to reach the edges) */
    if (nn) {
        static q16 acc;
        acc += fmul(FXC(1.0) + fmul(FXC(20), g3a.onset) + fmul(FXC(2.5), g3a.lev), g3_dt);
        n = (uint32_t)(acc >> 16);
        acc -= (q16)(n << 16);
    }
    for (i = 0; i < n; i++) {
        g3p_t *p = g3_spawn();
        q16 a, rg, rr, v;
        if (nn) {                                      /* a note: its place on the circle, its colour, its speed */
            q16 pick = fmul((q16)(g3_rnd() >> 16), wsum), acc = 0;
            uint32_t q = 0;
            int32_t note;
            while (q + 1u < nn && acc + nt[q].w < pick)
                acc += nt[q++].w;
            note = nt[q].n;
            rr = fclamp(fdiv((note - 24) << 16, FXC(72)));
            a = FXC(1.570796 + 0.25) + fmul(rr, FXC(6.283185 - 0.5)) + g3_norm(FXC(0.12));
            rg = fdiv((note - 28) << 16, FXC(56));
        } else {
            a = g3_uni(0, FXC(6.283185));
            rg = g3a.cent;
            rr = fclamp(rg);
        }
        v = fmul(fmul(FXC(1.8) + fmul(FXC(4.0), fpow(rr, FXC(1.4))), FXC(0.6) + fmul(FXC(0.4), g3a.lev)), g3_uni(FXC(0.6), FXC(1.0)));
        SX(p, 0);
        SY(p, 0);
        SVX(p, fmul(fcos(TURN(a)), v));
        SVY(p, fmul(fsin(TURN(a)), v));
        SAGE(p, FXC(0.2));
        SLIFE(p, 65536);
        p->c = g3_ramp(G3_COLDWARM, 6, rg + g3_uni(FXC(-0.06), FXC(0.06)));
    }
    for (i = 0; i < G3_NP; i++) {                     /* slow: they drift out */
        g3p_t *p = &g3pt[i];
        q16 k, d;
        int32_t x, y;
        if (!p->life)
            continue;
        SAGE(p, PAGE(p) + fmul(FXC(0.011), g3_dt));
        d = FXC(2.5) - fmul(PAGE(p), FXC(1.6));
        k = fdiv(65536, d < FXC(0.3) ? FXC(0.3) : d);
        SX(p, PX(p) + fmul(PVX(p), fmul(FXC(0.02), g3_dt)));
        SY(p, PY(p) + fmul(PVY(p), fmul(FXC(0.02), g3_dt)));
        SLIFE(p, fmul(PLIFE(p), 65536 - fmul(FXC(0.005), g3_dt)));
        x = (FXC(120) + fmul(fmul(PX(p), FXC(40)), k)) >> 8;
        y = (FXC(61) + fmul(fmul(PY(p), FXC(30)), k)) >> 8;
        if (PLIFE(p) < FXC(0.05) || x < -1280 || x > 62720 || y < -1280 || y > 32500) {
            p->life = 0;
            continue;
        }
        g3_dot(x, y, 150, g3_dim(p->c, PLIFE(p)));
    }
}

/* FLOWER: the wave wound into a flower, smoothed; more petals when brighter, its size the level, its line thicker the
 * wider it opens; the colour wheel along it, a soft blend; 4 faint ghosts; sparks from the petals' tips */
#define G3_FG 5u
#define G3_FPTS 60u
static struct { int8_t m[G3_FPTS]; uint8_t lv, petals; uint32_t rot; } g3flw[G3_FG] __attribute__((section(".pool")));
static uint32_t g3flw_n;
static __attribute__((minsize)) void g3_flower_shape(uint32_t s, q16 sc, int32_t ghost, int32_t *tipx, int32_t *tipy)
{
    uint32_t petals = g3flw[s].petals, p, i;
    q16 lv = g3flw[s].lv * 257, size = FXC(20) + fmul(FXC(26), lv), lw = FXC(1.0) + fmul(FXC(2.3), lv);
    for (p = 0; p < petals; p++) {
        int32_t px = 0, py = 0;
        q16 best = -1;
        for (i = 0; i <= G3_FPTS; i++) {
            uint32_t a = g3flw[s].rot + (p * G3_FPTS + i) * (0xFFFFFFFFu / (petals * G3_FPTS));
            q16 r = size + fmul(fmul(g3flw[s].m[i % G3_FPTS] * 516, FXC(16)), FXC(0.4) + fmul(FXC(0.6), lv));
            q16 x = fmul(fmul(fmul(r, fcos(a)), FXC(1.15)), sc), y = fmul(fmul(r, fsin(a)), sc);
            int32_t X = (FXC(120) + x) >> 8, Y = (FXC(61) + y) >> 8;
            uint16_t c = g3_hsv(g3_atan2(x, -y), FXC(0.92), 65536);   /* (the wheel by the angle from the top) */
            if (i) {
                if (ghost)
                    g3_line(px, py, X, Y, 256 * 3, c);
                else
                    g3_gline(px, py, X, Y, (int32_t)(lw >> 8), c, 70);
            }
            if (tipx && r > best) {
                best = r;
                tipx[p] = x;
                tipy[p] = y;
            }
            px = X;
            py = Y;
        }
    }
}
static __attribute__((minsize)) void g3s_flower(void)
{
    static const q16 SZ[5] = {FXC(0.45), FXC(0.7), FXC(1.05), FXC(1.6), FXC(2.2)};
    uint32_t s = g3flw_n % G3_FG, i, k, n;
    int32_t tipx[12], tipy[12], mx = 1, j;
    int32_t raw[G3_FPTS];
    g3_own(2);
    for (i = 0; i < G3_FPTS; i++) {                     /* the wave, smoothed (a mean over 17 samples) */
        q16 acc = 0;
        for (j = -8; j <= 8; j++)
            acc += g3_mid((uint32_t)((int32_t)i * 5 + 8 + j)) / 17;
        raw[i] = acc;
        if ((acc < 0 ? -acc : acc) > mx) mx = acc < 0 ? -acc : acc;
    }
    for (i = 0; i < G3_FPTS; i++)                      /* (normalised: the petals' depth the shape's, not the level's) */
        g3flw[s].m[i] = (int8_t)(raw[i] * 127 / mx);
    g3flw[s].lv = (uint8_t)(g3a.lev >> 8 > 255 ? 255 : g3a.lev >> 8);
    g3flw[s].petals = (uint8_t)(3 + (fmul(g3a.cent, FXC(9)) >> 16));
    if (g3flw[s].petals > 12) g3flw[s].petals = 12;
    g3flw[s].rot = fm1_ms * 238609u;                    /* (t * 0.35 rad) */
    g3flw_n++;
    for (k = G3_FG - 1u; k >= 1u; k--) {               /* the ghosts: a short echo, growing a little, fading fast */
        uint32_t gs;
        q16 al;
        if (k >= g3flw_n)
            continue;
        gs = (g3flw_n - 1u - k) % G3_FG;
        al = fmul(fpow(65536 - 65536 * (int32_t)k / 5, FXC(1.6)), fmul(FXC(0.35) + fmul(FXC(0.65), g3flw[gs].lv * 257), FXC(0.3)));
        g3_add = 1;
        g3_alpha = (int32_t)(al >> 8);
        g3_flower_shape(gs, 65536 + FXC(0.035) * (int32_t)k, 1, 0, 0);
        g3_alpha = 256;
        g3_add = 0;
    }
    g3_flower_shape(s, 65536, 0, tipx, tipy);
    n = (uint32_t)((fmul(FXC(40), g3a.onset) + fmul(fmul(FXC(5), g3a.lev), g3_uni(FXC(0.3), FXC(1.5)))) >> 16);
    for (i = 0; i < n; i++) {                          /* sparks from the tips */
        g3p_t *p = g3_spawn();
        uint32_t t = g3_rnd() % g3flw[s].petals, r = g3_rnd() % 100u, an;
        q16 sp = g3_uni(FXC(0.35), FXC(1.0));
        an = g3_atan2(tipy[t], tipx[t]) + TURN(g3_norm(FXC(0.35)));
        SX(p, tipx[t]);
        SY(p, tipy[t]);
        SVX(p, fmul(fcos(an), sp));
        SVY(p, fmul(fsin(an), sp));
        SLIFE(p, 65536);
        p->c = g3_hsv(g3_atan2(tipx[t], -tipy[t]), FXC(0.85), 65536);
        p->a = (uint8_t)(r < 30u ? 0 : r < 60u ? 1 : r < 80u ? 2 : r < 93u ? 3 : 4);
    }
    for (i = 0; i < G3_NP; i++) {
        g3p_t *p = &g3pt[i];
        int32_t ox, oy, x, y;
        uint16_t c;
        if (!p->life)
            continue;
        ox = (FXC(120) + PX(p)) >> 8;
        oy = (FXC(61) + PY(p)) >> 8;
        SX(p, PX(p) + fmul(PVX(p), g3_dt));
        SY(p, PY(p) + fmul(PVY(p), g3_dt));
        SLIFE(p, fmul(PLIFE(p), 65536 - fmul(FXC(0.025), g3_dt)));
        x = (FXC(120) + PX(p)) >> 8;
        y = (FXC(61) + PY(p)) >> 8;
        if (PLIFE(p) < FXC(0.07) || x < -1280 || x > 62720 || y < -1280 || y > 32500) {
            p->life = 0;
            continue;
        }
        c = g3_dim(p->c, FXC(0.3) + fmul(FXC(0.7), PLIFE(p)));
        if (p->a >= 2)
            g3_dot(x, y, (int32_t)(fmul(fmul(SZ[p->a], FXC(0.5)), FXC(0.5) + fmul(FXC(0.5), PLIFE(p))) >> 8), c);
        else
            g3_line(ox, oy, x, y, (int32_t)(SZ[p->a] >> 8), c);
    }
}

/* BLOCKS: the spectrum as blocks in relief, lows left, highs right, the last ones going back */
static __attribute__((minsize)) void g3s_blocks(void)
{
    static const g3pj_t C = {FXC(120), FXC(10), FXC(200), FXC(3.2), FXC(2.2), FXC(0.62)};
    int32_t j, b;
    for (j = 15; j >= 0; j--) {                        /* the far rows first */
        const uint8_t *sp = G3_HSV((uint32_t)j);
        q16 z = FXC(0.42) * j, fade = 65536 - 65536 * j / 16;
        for (b = 0; b < G3_HB; b++) {
            q16 v = sp[b] * 257, x0 = FXC(-2.0) + FXC(4.0) * b / G3_HB, x1 = FXC(-2.0) + fdiv(FXC(4.0) * b + FXC(3.4), FXC(G3_HB)) ;
            q16 top = FXC(-0.8) + fmul(v, FXC(1.6));
            int32_t ax, ay, bx, by, cx0, cy0, cx1, cy1, tax, tay, tbx, tby;
            uint16_t c = g3_ramp(G3_HOT, 5, v);
            g3_pj(&C, x0, top, z, &ax, &ay);
            g3_pj(&C, x1, top, z, &bx, &by);
            g3_pj(&C, x0, FXC(-0.8), z, &cx0, &cy0);
            g3_pj(&C, x1, FXC(-0.8), z, &cx1, &cy1);
            g3_pj(&C, x0, top, z + FXC(0.3), &tax, &tay);
            g3_pj(&C, x1, top, z + FXC(0.3), &tbx, &tby);
            g3_quad(tax, tay, tbx, tby, bx, by, ax, ay, g3_dim(c, fmul(FXC(0.55), fade) + FXC(0.1)), 256);
            g3_quad(ax, ay, bx, by, cx1, cy1, cx0, cy0, g3_dim(c, fmul(FXC(0.9), fade) + FXC(0.1)), 256);
        }
    }
}

/* CASCADE (OSCILLATORS): the last waveforms receding to the horizon, the nearer hiding the farther */
static uint32_t g3cas_n;
static __attribute__((minsize)) void g3s_cascade(void)
{
    static const g3pj_t C = {FXC(120), FXC(-2), FXC(200), FXC(3.2), FXC(2.2), FXC(0.62)};
    enum { NL = 14, NP = 72 };
    uint32_t j, i, slot = g3cas_n % NL;
    static int32_t sx[NP], sy[NP];
    for (i = 0; i < NP; i++) {
        q16 m = g3_mid(i * 3u) * 120 >> 16;
        g3w.cas.w[slot][i] = (int8_t)(m > 127 ? 127 : m < -127 ? -127 : m);
    }
    g3cas_n++;
    for (i = 0; i < 240u; i++)
        g3w.cas.hor[i] = (int16_t)cv_h;
    g3_clip = 1;
    for (j = 0; j < NL && j < g3cas_n; j++) {         /* front to back: each drawn above the nearer ones only */
        const int8_t *wv = g3w.cas.w[(g3cas_n - 1u - j) % NL];
        q16 z = FXC(0.42) * (int32_t)j, k = 65536 - 65536 * (int32_t)j / NL;
        k = FXC(0.25) + fmul(FXC(0.75), fmul(fmul(k, k), k));
        for (i = 0; i < NP; i++)
            g3_pj(&C, FXC(3.52) * (int32_t)i / (NP - 1) - FXC(1.76), wv[i] * FXC(0.8) / 120, z, &sx[i], &sy[i]);
        for (i = 0; i < 240u; i++)
            g3w.cas.top[i] = 0x7FFF;
        for (i = 1; i < NP; i++)
            g3_line(sx[i - 1], sy[i - 1], sx[i], sy[i], j ? 256 : 420, g3_dim(G3_ORANGE, k));
        for (i = 0; i < 240u; i++)
            if (g3w.cas.top[i] < g3w.cas.hor[i])
                g3w.cas.hor[i] = g3w.cas.top[i];
    }
    g3_clip = 0;
}

/* RIBBON (POLY-MOD): its envelope (ATTACK DECAY SUSTAIN, the decay again as release) as a ribbon, swaying */
static q16 g3r_L, g3r_cy, g3r_sy;
static __attribute__((minsize)) void g3_rb(q16 u, q16 v, q16 w, int32_t *X, int32_t *Y)
{
    static const g3pj_t C = {FXC(120), FXC(22), FXC(240), FXC(3.2), FXC(1.1), FXC(0.62)};
    q16 x = fmul(fdiv(u - g3r_L / 2, g3r_L), FXC(2.54)), y = fmul(v, FXC(1.1)) - FXC(0.45);
    q16 xr = fmul(x, g3r_cy) + fmul(w, g3r_sy), zr = -fmul(x, g3r_sy) + fmul(w, g3r_cy);
    g3_pj(&C, fmul(xr, FXC(1.1)), fmul(y, FXC(1.6)), zr + 65536, X, Y);
}
static __attribute__((minsize)) void g3s_ribbon(const track_t *t)
{
    const page_t *pg = cur_page();
    q16 a = FXC(0.06) + t->p[pg->id[0]] * FXC(0.55) / 127, d = FXC(0.1) + t->p[pg->id[1]] * FXC(0.8) / 127;
    q16 s = t->p[pg->id[2]] * 65536 / 127, r = FXC(0.1) + t->p[pg->id[3] != 0xFFu ? pg->id[3] : pg->id[1]] * FXC(0.9) / 127;
    q16 L = a + d + FXC(0.55) + r, depth = FXC(0.42);
    uint32_t yaw = (uint32_t)(sine_i(fm1_ms * 715828u) * 11469);   /* (+-0.55 rad, a sway in 6 s) */
    static int32_t fx_[64], fy_[64], bx_[64], by_[64];
    int32_t i, x0, y0, x1, y1;
    g3r_L = L;
    g3r_cy = fcos(yaw);
    g3r_sy = fsin(yaw);
#define G3RB(u, v, w, X, Y) g3_rb((u), (v), (w), &(X), &(Y))
    for (i = 0; i < 64; i++) {
        q16 u = L * i / 63, v;
        if (u <= a) v = fdiv(u, a);
        else if (u <= a + d) v = s + fmul(65536 - s, fexp(-fmul(FXC(4.6), fdiv(u - a, d))));
        else if (u <= a + d + FXC(0.55)) v = s;
        else v = fmul(s, fexp(-fmul(FXC(4.6), fdiv(u - a - d - FXC(0.55), r))));
        G3RB(u, v, -depth, fx_[i], fy_[i]);
        G3RB(u, v, depth, bx_[i], by_[i]);
    }
    G3RB(0, 0, depth, x0, y0);
    G3RB(L, 0, depth, x1, y1);
    g3_line(x0, y0, x1, y1, 256, T_RAISE);
    for (i = 0; i < 64; i += 3)
        g3_line(bx_[i], by_[i], fx_[i], fy_[i], 256, g3_dim(G3_VIOLET, FXC(0.28)));
    for (i = 1; i < 64; i++)
        g3_line(bx_[i - 1], by_[i - 1], bx_[i], by_[i], 256, g3_dim(G3_VIOLET, FXC(0.45)));
    for (i = 1; i < 64; i++)
        g3_gline(fx_[i - 1], fy_[i - 1], fx_[i], fy_[i], 460, G3_VIOLET, 90);
    G3RB(a, 65536, -depth, x0, y0);
    g3_dot(x0, y0, 768, G3_WHITE);
    G3RB(a + d, s, -depth, x0, y0);
    g3_dot(x0, y0, 768, G3_WHITE);
    G3RB(a + d + FXC(0.55), s, -depth, x0, y0);
    g3_dot(x0, y0, 768, G3_WHITE);
#undef G3RB
}

/* HELIX (LFO 2): the LFO's wave wound round a helix, turning with it */
static __attribute__((minsize)) void g3s_helix(const track_t *t)
{
    static const g3pj_t C = {FXC(120), FXC(0), FXC(230), FXC(3.2), FXC(1.6), FXC(0.62)};
    const uint32_t n = 200u, turns = 5u;
    uint32_t i;
    int32_t px = 0, py = 0, a0x, a0y, a1x, a1y;
    g3_pj(&C, FXC(-1.6), 0, FXC(0.9) - FXC(0.56), &a0x, &a0y);   /* the axis */
    g3_pj(&C, FXC(1.6), 0, FXC(0.9) + FXC(0.56), &a1x, &a1y);
    g3_line(a0x, a0y, a1x, a1y, 256, T_RAISE);
    for (i = 0; i < n; i++) {
        uint32_t cyc = i * (turns * (0xFFFFFFFFu / (n - 1u))) + t->lfo_ph;   /* (the wave's phase here: wraps, as a phase) */
        int32_t w, X, Y;
        q16 r, x, y, z, s, k;
        w = lfo_wave((track_t *)t, cyc);
        if (t->p[P_LWAVE] == 4)
            w = (int32_t)(((i * turns * 4u / n) * 2654435761u) >> 16) - 32768;
        r = FXC(0.55) + fmul(FXC(0.28), w * 2);
        s = fsin(cyc);
        x = FXC(3.2) * (int32_t)i / (int32_t)(n - 1u) - FXC(1.6);
        y = fmul(fmul(r, fcos(cyc)), FXC(1.3));
        z = fmul(fmul(r, s), FXC(1.3)) + FXC(0.9) + fmul(x, FXC(0.35));
        g3_pj(&C, x, y, z, &X, &Y);
        k = FXC(0.35) + fmul(FXC(0.65), FXC(0.5) - s / 2);
        if (i)
            g3_line(px, py, X, Y, (int32_t)((FXC(0.8) + fmul(FXC(1.2), k)) >> 8), g3_dim(G3_CYAN, k));
        px = X;
        py = Y;
    }
}

/* ----------------------------------------------------------------------------------------------- ENV --- */
/* the real envelope: the level of the last 4 s as a mountain; its fill forms going left from the present, its edge
 * slanting back and down from it; at the present an orb of light, growing with the level and on each attack, a small
 * spark in silence */
static const g3pj_t G3_CENV = {FXC(120), FXC(8), FXC(200), FXC(3.2), FXC(1.6), FXC(0.62)};
static __attribute__((minsize)) void g3_env_pt(int32_t i, q16 v, q16 w, int32_t *X, int32_t *Y)
{
    g3_pj(&G3_CENV, fmul(FXC(-3.9) + FXC(5.9) * i / (int32_t)(G3_HL - 1), FXC(0.95)) + fmul(w, FXC(0.6)),
          FXC(-0.9) + fmul(v, FXC(1.9)), FXC(0.6) + w, X, Y);
}
static __attribute__((minsize)) void g3s_env(uint16_t col)
{
    const int32_t n = G3_HL;
    const q16 depth = FXC(0.5);
    int32_t *lx = g3w.env.lx, *ly = g3w.env.ly;
    int32_t i, q;
    for (i = 0; i < n - 1; i++) {
        q16 v0 = G3_HLV((uint32_t)(n - 1 - i)) * 257, v1 = G3_HLV((uint32_t)(n - 2 - i)) * 257, u = 65536 - 65536 * i / (n - 1);
        for (q = 0; q < 6; q++) {                      /* the top, in strips front to back */
            q16 w0 = -depth + 2 * depth * q / 6, w1 = -depth + 2 * depth * (q + 1) / 6, e = 65536 * (2 * q + 1) / 12;
            q16 f = fclamp(fdiv(u - fmul(FXC(0.15), e), FXC(0.30)));
            int32_t x[4], y[4];
            if (!f) continue;
            g3_env_pt(i, v0, w1, &x[0], &y[0]);
            g3_env_pt(i + 1, v1, w1, &x[1], &y[1]);
            g3_env_pt(i + 1, v1, w0, &x[2], &y[2]);
            g3_env_pt(i, v0, w0, &x[3], &y[3]);
            g3_fill(x, y, 4, g3_dim(col, fmul(FXC(0.12) + fmul(FXC(0.35), v0), fpow(f, FXC(1.3)))), 256);
        }
        for (q = 0; q < 10; q++) {                     /* the front, in strips top to bottom */
            q16 h0 = 65536 - 65536 * q / 10, h1 = 65536 - 65536 * (q + 1) / 10, e = 65536 * (2 * q + 1) / 20;
            q16 f = fclamp(fdiv(u - fmul(FXC(0.15), e), FXC(0.30)));
            int32_t x[4], y[4];
            if (!f) continue;
            g3_env_pt(i, fmul(v0, h0), -depth, &x[0], &y[0]);
            g3_env_pt(i + 1, fmul(v1, h0), -depth, &x[1], &y[1]);
            g3_env_pt(i + 1, fmul(v1, h1), -depth, &x[2], &y[2]);
            g3_env_pt(i, fmul(v0, h1), -depth, &x[3], &y[3]);
            g3_fill(x, y, 4, g3_dim(col, fmul(FXC(0.4), fpow(f, FXC(1.3)))), 256);
        }
    }
    for (i = 0; i < n; i++)
        g3_env_pt(i, G3_HLV((uint32_t)(n - 1 - i)) * 257, -depth, &lx[i], &ly[i]);
    for (i = 0; i < n - 1; i++)
        g3_gline(lx[i], ly[i], lx[i + 1], ly[i + 1], 461, col, 120);
    {                                                  /* the orb */
        q16 lv = g3a.lev, r = FXC(0.9) + fmul(FXC(1.3), lv) + fmul(FXC(1.6), g3a.onset), vis = fclamp(FXC(0.45) + fmul(FXC(1.6), lv) + g3a.onset);
        int32_t rq = (int32_t)(r >> 8), ox = lx[n - 1], oy = ly[n - 1];
        g3_halo(ox, oy, rq * 13 / 10, G3_WHITE, (int32_t)(fmul(FXC(0.85), vis) >> 8));
        g3_halo(ox, oy, rq * 35 / 10, G3_WHITE, (int32_t)(fmul(FXC(0.32), vis) >> 8));
        g3_halo(ox, oy, rq * 6, G3_WHITE, (int32_t)(fmul(FXC(0.12), vis) >> 8));
        g3_dot(ox, oy, rq * 3 / 4, g3_dim(G3_WHITE, vis));
    }
}

/* FLT ENV: a plate of 24 x 24 columns tipped toward us, turning slowly; the spectrum spreads from the middle (now) to
 * the edges and corners (the past); round it the bands (lows at the back, the left channel on the left); aurora colours
 * by height */
static q16 g3p_cyw, g3p_syw, g3p_cpi, g3p_spi;
static __attribute__((minsize)) void g3_plate_pt(q16 x, q16 y, q16 z, int32_t *X, int32_t *Y)
{
    q16 X_ = fmul(x, g3p_cyw) - fmul(z, g3p_syw), Z_ = fmul(x, g3p_syw) + fmul(z, g3p_cyw), Y_ = y + FXC(0.6);
    q16 y2 = fmul(Y_, g3p_cpi) + fmul(Z_, g3p_spi), z2 = -fmul(Y_, g3p_spi) + fmul(Z_, g3p_cpi);
    q16 k = fdiv(FXC(128), FXC(4.2) + z2);
    *X = (FXC(120) + fmul(fmul(X_, k), FXC(1.15))) >> 8;
    *Y = (FXC(60) - fmul(y2, k)) >> 8;
}
static __attribute__((minsize)) void g3s_fenv(void)
{
    enum { N = 24 };
    uint16_t *order = g3w.plate.order;
    uint32_t yaw = fm1_ms * 102261u;                    /* (t * 0.15 rad) */
    q16 cell = FXC(3.2) / N, base = FXC(-0.6);
    int32_t i, b, j, cnt[64], pos[64];
    g3p_cyw = fcos(yaw);
    g3p_syw = fsin(yaw);
    g3p_cpi = fcos(TURN(FXC(0.95)));
    g3p_spi = fsin(TURN(FXC(0.95)));
    for (i = 0; i < 64; i++)
        cnt[i] = 0;
    for (j = 0; j < N; j++)                            /* the columns, far first: a bucket sort on depth */
        for (b = 0; b < N; b++) {
            q16 x0 = cell * (b - N / 2) + cell / 2, z0 = cell * (j - N / 2) + cell / 2;
            int32_t d = (fmul(x0, g3p_syw) + fmul(z0, g3p_cyw) + FXC(2.4)) / (FXC(4.8) / 63);
            d = d < 0 ? 0 : d > 63 ? 63 : d;
            cnt[d]++;
        }
    pos[63] = 0;
    for (i = 62; i >= 0; i--)
        pos[i] = pos[i + 1] + cnt[i + 1];
    for (j = 0; j < N; j++)                            /* (the depth again: not kept) */
        for (b = 0; b < N; b++) {
            q16 x0 = cell * (b - N / 2) + cell / 2, z0 = cell * (j - N / 2) + cell / 2;
            int32_t d = (fmul(x0, g3p_syw) + fmul(z0, g3p_cyw) + FXC(2.4)) / (FXC(4.8) / 63);
            d = d < 0 ? 0 : d > 63 ? 63 : d;
            order[pos[d]++] = (uint16_t)(j * N + b);
        }
    for (i = 0; i < N * N; i++) {
        static const uint8_t CX[4] = {0, 1, 1, 0}, CZ[4] = {0, 0, 1, 1};
        int32_t id = order[i], bb = id % N, jj = id / N, k, age, band, side;
        q16 cx = FXC(1) * bb - FXC(N / 2) + FXC(0.5), cz = FXC(1) * jj - FXC(N / 2) + FXC(0.5);
        q16 rr = fdiv(fhypot(cx, cz), FXC(N / 2 * 1.414)), v, top, fade, xs[2], zs[2];   /* (the history: 31 back at the corners) */
        uint32_t th = g3_atan2(cx, -cz);              /* (0 the back, + to the right) */
        uint16_t c;
        age = (int32_t)(fmul(fclamp(rr), FXC(31)) >> 16);
        side = (int32_t)th >= 0 ? 1 : 0;
        band = (int32_t)(((uint64_t)((int32_t)th < 0 ? 0u - th : th) * (uint32_t)G3_HB) >> 31);
        if (band > G3_HB - 1) band = G3_HB - 1;
        v = G3_HCV(side, (uint32_t)age)[band] * 257;
        top = base + FXC(0.02) + fmul(v, FXC(1.1));
        fade = FXC(0.3) + fmul(FXC(0.7), fpow(65536 - fclamp(rr), FXC(0.8)));
        c = g3_ramp(G3_AURORA, 5, FXC(0.12) + fmul(FXC(0.88), v));
        xs[0] = cell * (bb - N / 2);
        xs[1] = xs[0] + fmul(cell, FXC(0.88));
        zs[0] = cell * (jj - N / 2);
        zs[1] = zs[0] + fmul(cell, FXC(0.88));
        {
            int32_t tx[4], ty[4], bxs[4], bys[4];      /* (the corners once: top and base) */
            uint16_t cs = g3_dim(c, fmul(FXC(0.55), fade));
            for (k = 0; k < 4; k++) {
                g3_plate_pt(xs[CX[k]], top, zs[CZ[k]], &tx[k], &ty[k]);
                g3_plate_pt(xs[CX[k]], base, zs[CZ[k]], &bxs[k], &bys[k]);
            }
            for (k = 0; k < 4; k++) {                  /* the sides facing us */
                int32_t k2 = (k + 1) % 4;
                q16 mx = (xs[CX[k]] + xs[CX[k2]]) / 2 - (xs[0] + xs[1]) / 2, mz = (zs[CZ[k]] + zs[CZ[k2]]) / 2 - (zs[0] + zs[1]) / 2;
                if (fmul(mx, g3p_syw) + fmul(mz, g3p_cyw) < 0)
                    g3_quad(bxs[k], bys[k], bxs[k2], bys[k2], tx[k2], ty[k2], tx[k], ty[k], cs, 256);
            }
            g3_fill(tx, ty, 4, g3_dim(c, fmul(FXC(0.95), fade)), 256);
        }
    }
}

/* ----------------------------------------------------------------------------------------------- LFO --- */
/* a ring whose thickness is the track's LFO wave round it (the wave travelling with the LFO), turning, glowing */
enum { G3_NR = 56, G3_NRP = 13 };
static q16 g3l_ct, g3l_st;
static __attribute__((minsize)) void g3_lfo_pt(uint32_t u, q16 r, uint32_t v, int32_t *X, int32_t *Y)
{
    q16 q = FXC(1.35) + fmul(r, fcos(v)), x = fmul(q, fcos(u)), y = fmul(q, fsin(u)), z = fmul(r, fsin(v));
    q16 y2 = fmul(y, g3l_ct) - fmul(z, g3l_st), z2 = fmul(y, g3l_st) + fmul(z, g3l_ct), k = fdiv(FXC(66), FXC(3.4) + z2);
    *X = (FXC(120) + fmul(fmul(x, k), FXC(1.3))) >> 8;
    *Y = (FXC(74) + fmul(fmul(y2, k), FXC(1.05))) >> 8;
}
static __attribute__((minsize)) void g3s_lfo(const track_t *t)
{
    int32_t *rz = g3w.lfo.rz;
    uint8_t *ord = g3w.lfo.ord;
    q16 *wv = g3w.lfo.wv, lv = g3a.lev;
    uint32_t rot = fm1_ms * 3865470u, ring, i;          /* (t * 0.9 rad) */
    int32_t g = (int32_t)(fmul(FXC(0.5) + fmul(FXC(0.7), lv), FXC(120)) >> 16);
    g3l_ct = fcos(TURN(FXC(1.12)));
    g3l_st = fsin(TURN(FXC(1.12)));
    for (ring = 0; ring < G3_NR; ring++) {
        uint32_t u = ring * (0xFFFFFFFFu / G3_NR) + rot, ph = t->lfo_ph + ring * (uint32_t)(3ull * 0x100000000ull / G3_NR);
        int32_t w = lfo_wave((track_t *)t, ph);
        if (t->p[P_LWAVE] == 4)
            w = (int32_t)((((ring * 12u / G3_NR) + (t->lfo_ph >> 30)) * 2654435761u) >> 16) - 32768;
        wv[ring] = fclamp(w + 32768);
        rz[ring] = fmul(fmul(FXC(1.35), fsin(u)), g3l_st);   /* (the ring's depth: its centre's) */
        ord[ring] = (uint8_t)ring;
    }
    for (i = 1; i < G3_NR; i++) {                      /* far rings first */
        uint8_t o = ord[i];
        int32_t k = (int32_t)i - 1;
        while (k >= 0 && rz[ord[k]] < rz[o]) {
            ord[k + 1] = ord[k];
            k--;
        }
        ord[k + 1] = o;
    }
    for (ring = 0; ring < G3_NR; ring++) {
        uint32_t r = ord[ring], u = r * (0xFFFFFFFFu / G3_NR) + rot;
        q16 near = fclamp(FXC(0.5) - fdiv(rz[r], FXC(2.8))), rad = FXC(0.22) + fmul(FXC(0.62), wv[r]);
        uint16_t c = g3_dim(G3_CYAN, FXC(0.25) + fmul(fmul(FXC(0.75), near), FXC(0.55) + fmul(FXC(0.45), wv[r])));
        int32_t px, py, x, y;
        g3_lfo_pt(u, rad, 0, &px, &py);
        for (i = 1; i < G3_NRP; i++) {
            g3_lfo_pt(u, rad, i * (0xFFFFFFFFu / (G3_NRP - 1)), &x, &y);
            g3_add = 1;                                /* the glow: a blue-cyan halo round the line */
            g3_alpha = g * 2 / 3;
            g3_line(px, py, x, y, 256 * 4, RGB(70, 150, 245));
            g3_alpha = 256;
            g3_add = 0;
            g3_line(px, py, x, y, (int32_t)((FXC(1.1) + fmul(FXC(0.6), near)) >> 8), c);
            px = x;
            py = y;
        }
    }
}

/* ---------------------------------------------------------------------------------------------- FILTER --- */
/* the spectrum's outline as a surface to the horizon, lit; below the cutoff lava (what passes), above it ice (what the
 * filter cuts); a glowing mesh over it; at the cutoff a thin slab of light, fading upward, brighter with the resonance,
 * a peak of light at its foot and sparks rising when the filter rings */
static const g3pj_t G3_CFLT = {FXC(120), FXC(4), FXC(200), FXC(3.2), FXC(2.0), FXC(0.62)};
static __attribute__((minsize)) void g3_flt_pt(q16 bb, q16 v, q16 jj, int32_t *X, int32_t *Y)   /* bb a band (of 48, Q16), jj a row (Q16) */
{
    g3_pj(&G3_CFLT, FXC(-2) + fdiv(fmul(FXC(4), bb), FXC(G3_NB)), FXC(-0.8) + fmul(v, FXC(1.5)), fmul(FXC(0.34), jj), X, Y);
}
static __attribute__((minsize)) void g3_flt_row(int32_t j, int32_t *x, int32_t *y)   /* row j's points (24, the bands in pairs) */
{
    int32_t b;
    for (b = 0; b < G3_HB; b++)
        g3_flt_pt(FXC(2) * b, g3w.flt.rv[j][b] * 257, FXC(1) * j, &x[b], &y[b]);
}
static __attribute__((minsize)) void g3s_filter(const track_t *t)
{
    enum { H = G3_HS, BH = G3_HB };
    uint8_t (*rv)[BH] = g3w.flt.rv;
    int32_t *ax = g3w.flt.sx[0], *ay = g3w.flt.sy[0], *bx_ = g3w.flt.sx[1], *by_ = g3w.flt.sy[1];
    int32_t j, b, q, s;
    q16 bc = fmul(FXC(G3_NB - 1), t->p[P_E4] * 516), rq = t->p[P_E5] * 516, lv = g3a.lev;
    const q16 TH = FXC(0.55);
    const uint16_t lc = RGB(120, 230, 255), lava = g3_ramp(G3_LAVA, 5, FXC(0.9)), ice = g3_ramp(G3_ICE, 4, FXC(0.9));
    g3_own(3);
    for (j = 0; j < H; j++)                            /* the rows, smoothed across */
        for (b = 0; b < BH; b++) {
            int32_t sum = 0, n = 0, k;
            for (k = -1; k <= 1; k++)
                if (b + k >= 0 && b + k < BH) {
                    sum += G3_HSV((uint32_t)j)[b + k];
                    n++;
                }
            rv[j][b] = (uint8_t)(sum / n);
        }
    g3_flt_row(H - 1, ax, ay);
    for (j = H - 1; j > 0; j--) {                      /* the surface, far to near: row j (a) and row j - 1 (b) */
        q16 fade = fpow(65536 - 65536 * j / H, FXC(1.3));
        int32_t *tx, *ty;
        g3_flt_row(j - 1, bx_, by_);
        for (b = 0; b + 1 < BH; b++) {
            q16 v = rv[j][b] * 257, slope = (rv[j][b + 1] - rv[j][b] + rv[j - 1][b] - rv[j][b]) * 257, light;
            int32_t x[4], y[4];
            int below = FXC(2) * b + FXC(1) < bc;
            light = FXC(0.45) + fmul(FXC(0.55), fclamp(FXC(0.5) - fmul(slope, FXC(3))));
            x[0] = ax[b]; y[0] = ay[b];
            x[1] = ax[b + 1]; y[1] = ay[b + 1];
            x[2] = bx_[b + 1]; y[2] = by_[b + 1];
            x[3] = bx_[b]; y[3] = by_[b];
            g3_fill(x, y, 4, g3_dim(below ? g3_ramp(G3_LAVA, 5, fmul(v, FXC(0.9))) : g3_ramp(G3_ICE, 4, fmul(v, FXC(0.9))), fmul(light, fade)), 256);
        }
        tx = ax; ty = ay;                              /* (row j - 1 becomes the far one) */
        ax = bx_; ay = by_;
        bx_ = tx; by_ = ty;
    }
    g3_add = 1;                                        /* the mesh, glowing: across */
    for (j = 0; j < H; j += 2) {
        q16 f = fmul(FXC(0.55), fpow(65536 - 65536 * j / H, FXC(1.3)));
        g3_flt_row(j, ax, ay);
        for (b = 0; b + 1 < BH; b++) {
            uint16_t c = FXC(2) * b + FXC(1) < bc ? lava : ice;
            g3_alpha = (int32_t)(f >> 8);
            g3_line(ax[b], ay[b], ax[b + 1], ay[b + 1], 256, c);
            g3_alpha = (int32_t)(f >> 10);
            g3_line(ax[b], ay[b], ax[b + 1], ay[b + 1], 256 * 4, c);
        }
    }
    for (b = 0; b < BH; b += 2) {                      /* .. and along */
        uint16_t c = FXC(2) * b < bc ? lava : ice;
        int32_t px, py, x, y;
        g3_flt_pt(FXC(2) * b, rv[0][b] * 257, 0, &px, &py);
        for (j = 1; j < H; j++) {
            g3_flt_pt(FXC(2) * b, rv[j][b] * 257, FXC(1) * j, &x, &y);
            g3_alpha = (int32_t)(fmul(FXC(0.35), fpow(65536 - 65536 * j / H, FXC(1.3))) >> 8);
            g3_line(px, py, x, y, 256, c);
            px = x;
            py = y;
        }
    }
    g3_alpha = 256;
    {                                                  /* the slab of light at the cutoff: two faces and its front edge */
        q16 ka = FXC(0.5) + fmul(FXC(0.5), rq), kg = fmul(FXC(0.6) + fmul(FXC(1.6), rq), FXC(0.5) + fmul(FXC(0.5), lv));
        q16 far = FXC(1) * (H * 45 / 100);
        for (q = 0; q < 24; q++) {
            q16 v0 = fdiv(FXC(0.75) + FXC(1.5) * q / 24, FXC(1.5)), v1 = fdiv(FXC(0.75) + FXC(1.5) * (q + 1) / 24, FXC(1.5));
            q16 fq = fpow(65536 - 65536 * q / 24, FXC(1.6)), fe = fpow(65536 - 65536 * q / 24, FXC(1.4));
            int32_t x[4], y[4];
            for (s = -1; s <= 1; s += 2) {
                q16 bb = bc + s * TH / 2;
                g3_flt_pt(bb, v0, 0, &x[0], &y[0]);
                g3_flt_pt(bb, v1, 0, &x[1], &y[1]);
                g3_flt_pt(bb, v1, far, &x[2], &y[2]);
                g3_flt_pt(bb, v0, far, &x[3], &y[3]);
                g3_fill(x, y, 4, lc, (int32_t)(fmul(fmul(FXC(45.0), fq), ka + kg) >> 16));
            }
            g3_flt_pt(bc - TH / 2, v0, 0, &x[0], &y[0]);
            g3_flt_pt(bc + TH / 2, v0, 0, &x[1], &y[1]);
            g3_flt_pt(bc + TH / 2, v1, 0, &x[2], &y[2]);
            g3_flt_pt(bc - TH / 2, v1, 0, &x[3], &y[3]);
            g3_fill(x, y, 4, lc, (int32_t)(fmul(fmul(FXC(190.0), fe), ka + kg / 2) >> 16));
        }
        for (s = -1; s <= 1; s += 2) {
            int32_t x0, y0, x1, y1;
            g3_flt_pt(bc + s * TH / 2, FXC(0.5), 0, &x0, &y0);
            g3_flt_pt(bc + s * TH / 2, FXC(0.5), far, &x1, &y1);
            g3_line(x0, y0, x1, y1, 256, lc);
        }
    }
    {                                                  /* the peak of light at its foot */
        int32_t bi = (int32_t)(bc >> 17), fx_, fy_;
        if (bi < 0) bi = 0;
        if (bi > BH - 1) bi = BH - 1;
        g3_flt_pt(bc, rv[0][bi] * 257 + FXC(0.05), 0, &fx_, &fy_);
        g3_halo(fx_, fy_, (int32_t)((FXC(1.5) + fmul(FXC(3), rq)) >> 8), G3_WHITE, (int32_t)(fmul(fmul(rq, FXC(0.4) + fmul(FXC(0.6), lv)), FXC(256)) >> 16));
    }
    g3_add = 0;
}

static __attribute__((minsize)) void g3_draw(uint32_t kind)
{
    const track_t *t = TSEL;
    static uint32_t last;
    cv_oy = 0;
    g3_add = 0;
    g3_alpha = 256;
    g3_dt = (q16)((fm1_ms - last) * 65536u / 40u);
    if (g3_dt < FXC(0.25) || g3_dt > FXC(4.0)) g3_dt = 65536;
    last = fm1_ms;
    g3_analyse();
    switch (kind) {
    case G3_HOME:
        switch (g3_style()) {
        case G3S_WALLS: g3s_walls(); break;
        case G3S_TUNNEL: g3s_tunnel(); break;
        case G3S_CELL: g3s_cell(); break;
        case G3S_WAVES: g3s_waves(); break;
        case G3S_SPARKS: g3s_sparks(); break;
        case G3S_FLOWER: g3s_flower(); break;
        case G3S_BLOCKS: g3s_blocks(); break;
        case G3S_CASCADE: g3s_cascade(); break;
        case G3S_RIBBON: g3s_ribbon(t); break;
        case G3S_HELIX: g3s_helix(t); break;
        default: g3s_disc(); break;
        }
        break;
    case G3_ENV:
        g3s_env(G3_PINK);
        break;
    case G3_FENV:
        g3s_fenv();
        break;
    case G3_LFO:
        g3s_lfo(t);
        break;
    case G3_FLT:
        g3s_filter(t);
        break;
    }
    g3_add = 0;
    g3_alpha = 256;
}
