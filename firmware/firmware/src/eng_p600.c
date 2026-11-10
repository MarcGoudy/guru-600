/* SPDX-License-Identifier: GPL-3.0-only */
/* P600: a Prophet-600 voice. Two oscillators per voice, each a sum of saw, triangle and pulse (any of the three),
 * OSC A hard-synced to OSC B, a mixer between them, a four-pole (24 dB/oct) resonant low-pass ladder with its own
 * ADSR, keyboard tracking (OFF / HALF / FULL, from the lowest C of the original's keyboard) and POLY-MOD: the filter
 * envelope and OSC B, each with its amount, to OSC A's frequency and / or the cutoff (OSC B at audio rate).
 * The amplitude is the host's ADSR, the LFO the host's (its PIT / FLT / SHP destinations: SHP is the pulse widths),
 * GLIDE and UNISON the host's VOICE page.
 *
 * Parameters: EDIT 1 (OSC) A WAV, A FRQ, B WAV, B FRQ; EDIT 2 (FILTER) CUT, RES, MIX, FENV. The rest of the original's
 * panel in the track parameters that only the retired DIGITAL used (P_FM1_ATK .. P_FM4_LEVEL, params.c P600_XDESC):
 *   FLT ENV   P_FM1_ATK DEC SUS REL      the filter envelope
 *   OSC 2     P_FM2_ATK DEC SUS REL      A PW, B PW, B FINE, SYNC
 *   POLY MOD  P_FM3_ATK DEC SUS          PM ENV (amount), PM B (amount), PM DST (OFF FRQ A, FILT, BOTH)
 *   FILTER    P_E4 E5 E7, P_FM3_REL      CUTOFF, RESONANCE, ENV AMOUNT and KBD tracking, as the panel's section
 *   MIXER     P_E6, P_GLIDE, P_VOICE     MIXER, GLIDE, UNISON (the host's voice modes)
 *   EXTRAS    P_FM4_ATK, P_M4AMT, P_M3AMT, P_DETUNE: not on the Prophet-600: VINTAGE, the mod wheel's vibrato (matrix
 *             slot 4, MODW -> VIB), velocity to the cutoff (slot 3, VEL -> CUT), the unison's detune (ui.c sets the
 *             slots with a factory program)
 * Voice state: s[0] s[1] s[6] s[7] the ladder's four stages, s[4] the filter envelope (Q24), s[5] its stage
 * (1 attack, 2 decay / sustain, 3 release, 0 idle), s[2] a per-voice drift seed, s[3] its hiss. ph[0] OSC A, ph[1] OSC B. */

enum { P6_A_WAV, P6_A_FRQ, P6_B_WAV, P6_B_FRQ, P6_CUT, P6_RES, P6_MIX, P6_FENV };
#define P6_FATK P_FM1_ATK
#define P6_FDEC P_FM1_DEC
#define P6_FSUS P_FM1_SUS
#define P6_FREL P_FM1_REL
#define P6_APW P_FM2_ATK
#define P6_BPW P_FM2_DEC
#define P6_BFIN P_FM2_SUS
#define P6_SYNC P_FM2_REL
#define P6_PMENV P_FM3_ATK
#define P6_PMB P_FM3_DEC
#define P6_PMDST P_FM3_SUS
#define P6_KBD P_FM3_REL
#define P6_VINT P_FM4_ATK        /* EXTRAS: VINTAGE, the analog instability: each voice's own detune and cutoff */

/* the waves an oscillator sums: bit 0 saw, 1 triangle, 2 pulse */
static const char *const N_P6_WAVE[] = {"OFF", "SAW", "TRI", "SAW+T", "PLS", "SAW+P", "TRI+P", "ALL"};
static const char *const N_P6_PMDST[] = {"OFF", "FRQ A", "FILT", "BOTH"};
static const char *const N_P6_KBD[] = {"OFF", "HALF", "FULL"};


/* G = g / (1 + g) of the one-pole stages for the cutoff values 0..127 (Q15), from the SVF's g (Q12): made once */
static uint16_t p6_gt[128];
static void p6_tables(void)
{
    uint32_t i;
    if (p6_gt[127])
        return;
    for (i = 0; i < 128u; i++)
        p6_gt[i] = (uint16_t)(((uint32_t)SVF_G[i] << 15) / (4096u + SVF_G[i]));
}
static inline int32_t p6_g(int32_t cut)                /* cut 0..127 << 8 */
{
    int32_t i, g;
    cut = clamp(cut, 0, 127 << 8);
    i = cut >> 8;
    g = p6_gt[i];
    if (i < 127)
        g += ((p6_gt[i + 1] - g) * (cut & 255)) >> 8;
    return g;
}

/* the ladder's coefficients: G, 1 - G, G^4 and 1 / (1 + k G^4) (Q15); k 0..4.3 (Q12) */
typedef struct { int32_t g, b, g4, inv, k; } p6lad_t;
static inline void p6_coef(p6lad_t *c, int32_t cut, int32_t k)
{
    int32_t g2;
    c->g = p6_g(cut);
    c->b = 32768 - c->g;
    g2 = mulq15(c->g, c->g);
    c->g4 = mulq15(g2, g2);
    c->k = k;
    c->inv = (int32_t)((1u << 30) / (uint32_t)(32768 + ((k * c->g4) >> 12)));
}

/* a * q (q Q15, at most 1.0) for a up to 2^20: a's three low bits go (32 bits, no overflow) */
static inline int32_t p6_mul(int32_t q, int32_t a) { return (q * (a >> 3) + 2048) >> 12; }
/* a * q rounded (not floored: the floor's dead zone would stop the faint signal a self-oscillation grows from) */
static inline int32_t p6_mq(int32_t q, int32_t a) { return (q * a + 16384) >> 15; }

/* one sample of the ladder (Zavalishin's zero-delay form, the input through tanh): in about +-16384, the stages
 * within +-65535 (b * 65535 fits 32 bits) */
static inline int32_t p6_ladder(const p6lad_t *c, int32_t in, int32_t *st)
{
    int32_t g = c->g, b = c->b, y, x, sig;
    sig = p6_mul(b, st[3] + p6_mul(g, st[2] + p6_mul(g, st[1] + p6_mul(g, st[0]))));
    y = p6_mul(c->inv, p6_mul(c->g4, in) + sig);
    x = softclip(in - ((c->k * y) >> 12));             /* the feedback, softly limited as the CEM3320's input */
    y = p6_mq(g, x) + p6_mq(b, st[0]);
    st[0] = clamp(2 * y - st[0], -65535, 65535);
    y = p6_mq(g, y) + p6_mq(b, st[1]);
    st[1] = clamp(2 * y - st[1], -65535, 65535);
    y = p6_mq(g, y) + p6_mq(b, st[2]);
    st[2] = clamp(2 * y - st[2], -65535, 65535);
    y = p6_mq(g, y) + p6_mq(b, st[3]);
    st[3] = clamp(2 * y - st[3], -65535, 65535);
    return y;
}

/* an oscillator's waves summed, at half scale each: w bit 0 saw, 1 triangle, 2 pulse of width pw */
static inline int32_t p6_osc(uint32_t w, uint32_t ph, uint32_t inc, uint32_t pw)
{
    int32_t s = 0;
    if (w & 1u)
        s += osc_saw(ph, inc);
    if (w & 2u)
        s += osc_tri(ph);
    if (w & 4u)
        s += osc_pulse(ph, inc, pw) << 1;
    return s >> 1;
}

/* Guru-600, EDIT > MORPH (ui.c mph_set): what a parameter cannot hold half way, the engine fades: each oscillator's
 * waves (A's sum and B's, k), SYNC (a soft sync, k of the way), POLY-MOD's destinations and KEYBOARD (their weights),
 * on track t while its parameters are still those the morph wrote (s[]: A WAV, B WAV, SYNC, PM DS, KBD) */
static volatile struct { const track_t *t; uint8_t a[5], b[5], s[5]; uint16_t k; } p6m;
static int32_t p6_osc_m(uint32_t w0, uint32_t w1, int32_t k, uint32_t ph, uint32_t inc, uint32_t pw)
{
    int32_t s = p6_osc(w0, ph, inc, pw);
    return w0 == w1 || !k ? s : s + (((p6_osc(w1, ph, inc, pw) - s) * k) >> 8);
}

/* a pulse width 0..127 (the original's knob: 64 square) as a phase offset, 2 % .. 98 %, plus the shape modulation */
static inline uint32_t p6_pw(int32_t v, int32_t shape)
{
    int32_t w = (v << 9) + ((shape - (64 << 8)) << 1);  /* Q16 of the cycle */
    return (uint32_t)clamp(w, 1311, 64225) << 16;
}


static void p600_note_on(track_t *t, voice_t *v)
{
    (void)t;
    v->ph[1] = v->ph[0] + 0x40000000u;
    if (!v->s[2])
        v->s[2] = (int32_t)(0x2468ACEu + v->age * 2654435761u);   /* the voice's drift */
    v->s[5] = 1;                                      /* the filter envelope attacks (from where it is) */
}

/* one control tick of the filter envelope (the host's curves: ENV_LIN, ENV_EXP); returns Q15 */
static int32_t p6_fenv(const int16_t *p, voice_t *v)
{
    int32_t e = v->s[4];
    if (!v->gate && v->s[5] && v->s[5] < 3)
        v->s[5] = 3;
    switch (v->s[5]) {
    case 1:
        e += (int32_t)ENV_LIN[p[P6_FATK] & 127];
        if (e >= (1 << 24)) {
            e = 1 << 24;
            v->s[5] = 2;
        }
        break;
    case 2:
        e += mulq16(((int32_t)p[P6_FSUS] << 17) - e, ENV_EXP[p[P6_FDEC] & 127]);
        break;
    case 3:
        e -= mulq16(e, ENV_EXP[p[P6_FREL] & 127]);
        if (e < (1 << 12)) {
            e = 0;
            v->s[5] = 0;
        }
        break;
    default:
        e = 0;
        break;
    }
    v->s[4] = e;
    return e >> 9;
}

static void p600_render(track_t *t, voice_t *v, int32_t *out, uint32_t n, const vmod_t *m)
{
    const int16_t *p = t->p;
    uint32_t wa = (uint32_t)p[P_E0 + P6_A_WAV] & 7u, wb = (uint32_t)p[P_E0 + P6_B_WAV] & 7u, i;
    uint32_t sync = p[P6_SYNC] != 0, dst = (uint32_t)p[P6_PMDST] & 3u;
    uint32_t wa1 = wa, wb1 = wb;
    int32_t mk = 0, ks = sync ? 256 : 0, wf = dst & 1u ? 256 : 0, wt = dst & 2u ? 256 : 0, kq = p[P6_KBD] * 256;
    int32_t fenv = p6_fenv(p, v);
    if (p6m.t == t && p6m.s[0] == (uint8_t)p[P_E0 + P6_A_WAV] && p6m.s[1] == (uint8_t)p[P_E0 + P6_B_WAV] &&
        p6m.s[2] == (uint8_t)p[P6_SYNC] && p6m.s[3] == (uint8_t)p[P6_PMDST] && p6m.s[4] == (uint8_t)p[P6_KBD]) {
        mk = p6m.k;                                   /* (Guru-600: MORPH, its fades) */
        wa = p6m.a[0] & 7u, wa1 = p6m.b[0] & 7u, wb = p6m.a[1] & 7u, wb1 = p6m.b[1] & 7u;
        ks = (p6m.a[2] ? 256 - mk : 0) + (p6m.b[2] ? mk : 0);
        wf = (p6m.a[3] & 1u ? 256 - mk : 0) + (p6m.b[3] & 1u ? mk : 0);
        wt = (p6m.a[3] & 2u ? 256 - mk : 0) + (p6m.b[3] & 2u ? mk : 0);
        kq = p6m.a[4] * (256 - mk) + p6m.b[4] * mk;
        sync = ks != 0;
        dst = (wf ? 1u : 0u) | (wt ? 2u : 0u);
    }
    int32_t vint = p[P6_VINT];                         /* VINTAGE 0..127: each voice off by up to +-20 cents, its */
    int32_t drift = (((int32_t)((uint32_t)v->s[2] >> 24) - 128) * vint * 3) >> 10;   /* cutoff by up to +-6 steps */
    int32_t cdrift = (((int32_t)(((uint32_t)v->s[2] >> 16) & 255u) - 128) * vint * 6) >> 6;
    int32_t pa = m->pitch16 + (p[P_E0 + P6_A_FRQ] - 24) * 16;
    int32_t pb = m->pitch16 + (p[P_E0 + P6_B_FRQ] - 24) * 16;
    int32_t pmenv = (fenv * p[P6_PMENV]) >> 7;        /* Q15 */
    int32_t pmb = p[P6_PMB] * (dst ? 1 : 0);
    int32_t kbd = ((kq >> 4) * (v->pitch16 - 36 * 16) * 150) >> 8;   /* FULL: 1.17 cutoff steps a semitone */
    int32_t cut = (p[P_E0 + P6_CUT] << 8) + m->cutoff + kbd + ((fenv * p[P_E0 + P6_FENV]) >> 7) + cdrift;
    int32_t k = p[P_E0 + P6_RES] * 23406 / 127;      /* 0 .. 5.7 (Q12): self-oscillation past 7 of 10 (k 4), as the
                                                        * original's manual says (CM600A 7-5) */
    int32_t comp = 4096 + (k >> 2);                   /* the ladder's passband loss, half made up */
    int32_t mb = p[P_E0 + P6_MIX] * 258, ma = 32767 - mb;
    uint32_t pwa = p6_pw(p[P6_APW], m->shape), pwb = p6_pw(p[P6_BPW], m->shape);
    uint32_t inca, incb, ph0 = v->ph[0], ph1 = v->ph[1];
    int32_t nz = v->s[3] ? v->s[3] : 0x13579BDF ^ (int32_t)(v->age * 2654435761u);   /* the voice's own hiss (s[3]):
                                                       * no state shared between the cores (2ND CORE) */
    int32_t st[4] = {v->s[0], v->s[1], v->s[6], v->s[7]};
    p6lad_t c;
    p6_tables();
    if (dst & 1u)
        pa += (((pmenv * 960) >> 15) * wf) >> 8;      /* PM ENV -> FRQ A: up to 5 octaves */
    if (dst & 2u)
        cut += (pmenv * wt) >> 8;                     /* PM ENV -> FILT */
    inca = pitch_inc(clamp(pa, 0, 2047));
    incb = cents_inc(clamp(pb, 0, 2047), p[P6_BFIN] * 100 / 127, 0);   /* B FINE: up to a semitone up */

    inca += (uint32_t)((int32_t)(inca >> 12) * (m->fine + drift));
    incb += (uint32_t)((int32_t)(incb >> 12) * (m->fine - drift));
    p6_coef(&c, cut, k);
    for (i = 0; i < n; i++) {
        int32_t b = p6_osc_m(wb, wb1, mk, ph1, incb, pwb), a, s;
        uint32_t ia = inca;
        if (pmb) {                                    /* POLY-MOD from OSC B at audio rate */
            int32_t src = wb ? b : osc_tri(ph1);
            int32_t d = (src * pmb) >> 7;             /* +-32767 at full */
            if (dst & 1u)
                ia = pitch_inc(clamp(pa + ((((d * 768) >> 15) * wf) >> 8), 0, 2047));   /* up to +-4 octaves */
            if ((dst & 2u) && !(i & 3u))              /* the cutoff every 4 samples (11 kHz): a divide less */
                p6_coef(&c, cut + (((d >> 1) * wt) >> 8), k);
        }
        a = p6_osc_m(wa, wa1, mk, ph0, ia, pwa);
        ph0 += ia;
        ph1 += incb;
        if (sync && ph1 < incb) {                     /* OSC B wrapped: OSC A restarts with it */
            uint32_t to = (ph1 / ((incb >> 16) | 1u)) * (ia >> 16);
            ph0 = ks >= 256 ? to : ph0 + (uint32_t)((((int32_t)(to - ph0)) >> 8) * ks);   /* (MORPH: part way) */
        }
        s = mulq15(a, ma) + mulq15(b, mb) + (int32_t)(noise32(&nz) >> 24) - 128;   /* the circuit's hiss:
                                                                     * what a self-oscillating filter starts from */
        s = (p6_ladder(&c, s >> 1, st) * comp) >> 11;   /* (x2: the level of the other engines) */
        out[i] += voice_amp(soft_knee(s, 16000), m, i) << 1;
    }
    v->ph[0] = ph0;
    v->ph[1] = ph1;
    v->s[3] = nz;
    v->s[0] = st[0];
    v->s[1] = st[1];
    v->s[6] = st[2];
    v->s[7] = st[3];
}

#include "p600_bank.h"
                         /* P600_PRESETS[]: the original's 100 factory programs, the free v2022 collection's 100, then
                          * 55 free places; P600_EXT[]: the rest of the fixed ones (p600/make_bank.py) */
#include "p600_sci.h"        /* Guru-600: the factory programs as Sequential sends them (p600_export) */

/* IMPORT: programs received as SysEx over USB (p600_sysex, from editor.c): a Prophet-600 program dump (Sequential's,
 * F0 01 02 nn + 32 nibbles F7) or a GliGli firmware's patch dump (F0 00 61 16 01 .. F7), each into a place of the
 * 255 (dest 0..254): the first free one (201..255 as shown), or the one a Guru 600 frame names (F0 7D 47 36 01 dest
 * dest2 <the dump's bytes> F7, the send page). Up to P6_NIMP of them, replacing a fixed program for as long as they
 * are there; kept in flash (p600_store.c, OBJ_P600) and put back at power-on. F0 7D 47 36 02 F7 forgets them all
 * (as MENU > RESET SOUNDS), 03 dest dest2 the one at dest; Guru-600: 04 dest dest2 asks for the place's sound
 * (p600_export), 05 for the places that hold a kept one (p600_list); SAVE > PLACE keeps a track's sound in a place
 * (p600_store_track). The presets the engine shows are a RAM copy of the table
 * with the imported ones in their places (p600_apply) */
#define P6_NIMP 55u
typedef struct {
    uint8_t dest, used;                                /* the place (0..254), 1 = in use */
    int8_t e[8];
    uint8_t env[4];
    p600_ext_t x;
    char name[16];
} p6imp_t;
#define P6ST_MAGIC 0x4D493650u                         /* "P6IM" */
typedef struct {                                       /* the imports as kept in flash (p600_store.c, OBJ_P600) */
    uint32_t magic;
    uint16_t ver, n;                                   /* 1, P6_NIMP */
    p6imp_t imp[P6_NIMP];
} p6st_t;
static p6st_t p6st __attribute__((section(".pool")));   /* (Guru-600 10/11: one copy, worked on and kept: 2.9 KB less) */
#define p6_imp (p6st.imp)
static preset_t p6_ram[255] __attribute__((section(".pool")));   /* the presets shown (after p600_boot) */
static uint8_t p6_booted, p6_dirty;                    /* p6_dirty: to be kept in flash (p600_store.c) */
static uint32_t p6_dirty_ms;
static engine_t ENG_P600;
static const p600_ext_t P6_EMPTY_EXT = {{0, 70, 64, 40}, {64, 64}, 0, 0, {0, 0, 0}, 2, {70, 1}, {63, 0, 0}, 0, 0, 0, 0, 12, 64};

static int32_t p6_find(uint32_t dest)                  /* the import in place dest, -1 none */
{
    uint32_t i;
    for (i = 0; i < P6_NIMP; i++)
        if (p6_imp[i].used && p6_imp[i].dest == dest)
            return (int32_t)i;
    return -1;
}

/* the presets shown: the table, each import in its place, the free places (201..255) shown up to the last one used */
static void p600_apply(void)
{
    uint32_t i, top = P600_NFIX;
    if (!p6_booted)
        return;
    for (i = 0; i < 255u; i++)
        p6_ram[i] = P600_PRESETS[i];
    for (i = 0; i < P6_NIMP; i++) {
        const p6imp_t *m = &p6_imp[i];
        uint32_t k;
        if (!m->used || m->dest >= 255u)
            continue;
        p6_ram[m->dest].name = m->name;
        for (k = 0; k < 8u; k++)
            p6_ram[m->dest].e[k] = m->e[k];
        for (k = 0; k < 4u; k++)
            p6_ram[m->dest].env[k] = m->env[k];
        p6_ram[m->dest].mono = 0;                      /* (Guru-600: a kept sound plays as a Prophet-600 sound, POLY or */
        for (k = 0; k < 4u; k++)                       /* its UNISON, dry (every send 0, stored + 1) like the factory */
            p6_ram[m->dest].fx[k] = 1;                 /* 1..200, whatever the place's own program had: never the */
                                                       /* replaced sound's MONO or effects) */
        p6_ram[m->dest].fenv = 0;
        if (m->dest + 1u > top)
            top = m->dest + 1u;
    }
    ENG_P600.presets = p6_ram;
    ENG_P600.npresets = (uint8_t)top;
}

static uint32_t p6_bits(const uint8_t *b, uint32_t *pos, uint32_t w)   /* w bits of b[], low first */
{
    uint32_t v = 0, i;
    for (i = 0; i < w; i++, (*pos)++)
        v |= (uint32_t)((b[*pos >> 3] >> (*pos & 7u)) & 1u) << i;
    return v;
}
static int32_t p6_clamp(int32_t v, int32_t lo, int32_t hi) { return v < lo ? lo : v > hi ? hi : v; }

/* Sequential's program dump: the Z80's 16 bytes, as gligli p600fw import.c reads them (p600/make_bank.py convert) */
static void p6_from_sci(const uint8_t *m, p6imp_t *o)
{
    static const uint8_t ENV_CV[16] = {0, 55, 86, 101, 111, 124, 135, 139, 143, 148, 154, 164, 176, 185, 191, 210};
    uint8_t b[16];
    uint32_t k, pos = 0;
    uint32_t pwA, pmF, lfoF, pmB, lfoA, fB, fA, fine, mix, cut, res, fea, fr, fs, fd, fa, ar, as, ad, aa, gl, pwB;
    uint32_t pA, pB, tF, tH, lS, lP, lW, lFl, sA, tA, sy, sB, tB, pFA, pFl, uni;
    int32_t depth;
    (void)ENV_CV;
    for (k = 0; k < 16u; k++)
        b[k] = (uint8_t)((m[3 + 2 * k] & 15u) | (m[4 + 2 * k] & 15u) << 4);
    pwA = p6_bits(b, &pos, 7); pmF = p6_bits(b, &pos, 4); lfoF = p6_bits(b, &pos, 4); pmB = p6_bits(b, &pos, 7);
    lfoA = p6_bits(b, &pos, 5); fB = p6_bits(b, &pos, 6); fA = p6_bits(b, &pos, 6); fine = p6_bits(b, &pos, 7);
    mix = p6_bits(b, &pos, 6); cut = p6_bits(b, &pos, 7); res = p6_bits(b, &pos, 6); fea = p6_bits(b, &pos, 4);
    fr = p6_bits(b, &pos, 4); fs = p6_bits(b, &pos, 4); fd = p6_bits(b, &pos, 4); fa = p6_bits(b, &pos, 4);
    ar = p6_bits(b, &pos, 4); as = p6_bits(b, &pos, 4); ad = p6_bits(b, &pos, 4); aa = p6_bits(b, &pos, 4);
    gl = p6_bits(b, &pos, 4); pwB = p6_bits(b, &pos, 7);
    pA = p6_bits(b, &pos, 1); pB = p6_bits(b, &pos, 1); tF = p6_bits(b, &pos, 1); tH = p6_bits(b, &pos, 1);
    lS = p6_bits(b, &pos, 1); lP = p6_bits(b, &pos, 1); lW = p6_bits(b, &pos, 1); lFl = p6_bits(b, &pos, 1);
    sA = p6_bits(b, &pos, 1); tA = p6_bits(b, &pos, 1); sy = p6_bits(b, &pos, 1); sB = p6_bits(b, &pos, 1);
    tB = p6_bits(b, &pos, 1); pFA = p6_bits(b, &pos, 1); pFl = p6_bits(b, &pos, 1); uni = p6_bits(b, &pos, 1);
    o->e[P6_A_WAV] = (int8_t)(sA | tA << 1 | pA << 2);
    o->e[P6_A_FRQ] = (int8_t)fA;
    o->e[P6_B_WAV] = (int8_t)(sB | tB << 1 | pB << 2);
    o->e[P6_B_FRQ] = (int8_t)fB;
    o->e[P6_CUT] = (int8_t)P6_CUT8[cut];
    o->e[P6_RES] = (int8_t)(res * 2u);
    o->e[P6_MIX] = (int8_t)(mix * 2u);
    o->e[P6_FENV] = (int8_t)p6_clamp((int32_t)fea * 137 / 15, 0, 127);
    o->env[0] = P6_Z80_ENV[aa]; o->env[1] = P6_Z80_ENV[ad]; o->env[2] = (uint8_t)(as * 127u / 15u); o->env[3] = P6_Z80_ENV[ar];
    o->x.fenv[0] = P6_Z80_ENV[fa]; o->x.fenv[1] = P6_Z80_ENV[fd]; o->x.fenv[2] = (uint8_t)(fs * 127u / 15u);
    o->x.fenv[3] = P6_Z80_ENV[fr];
    o->x.pw[0] = (uint8_t)pwA; o->x.pw[1] = (uint8_t)pwB; o->x.fine = (uint8_t)fine; o->x.sync = (uint8_t)sy;
    o->x.pm[0] = (uint8_t)(pmF * 127u / 15u); o->x.pm[1] = (uint8_t)pmB; o->x.pm[2] = (uint8_t)(pFA | pFl << 1);
    o->x.kbd = (uint8_t)(tF ? 2u : tH ? 1u : 0u);
    depth = (int32_t)(lfoA * lfoA * 63u / 961u);        /* (amt / 31)^2, as make_bank.py */
    o->x.lfo[0] = P6_Z80_LFO[lfoF]; o->x.lfo[1] = (uint8_t)(lS ? 1u : 3u);
    o->x.lfod[0] = (int8_t)(lP ? 63 : 0); o->x.lfod[1] = (int8_t)(lW ? 63 : 0); o->x.lfod[2] = (int8_t)(lFl ? 63 : 0);
    o->x.wheel = (uint8_t)p6_clamp(64 * (63 - depth) / 63, 0, 63);   /* INITIAL AMOUNT; the wheel opens the rest */
    o->x.glide = (uint8_t)(gl * 6u); o->x.unison = (uint8_t)uni; o->x.lfoamp = 0; o->x.vel = 0; o->x.detune = 12;
}

/* a GliGli patch dump (gligli p600fw midi.c / storage.c preset_loadCurrent; p600/make_bank.py convert_gligli) */
static uint32_t p6_rd16(const uint8_t *b, uint32_t i) { return (uint32_t)b[i] | (uint32_t)b[i + 1] << 8; }
static void p6_from_gligli(const uint8_t *buf, p6imp_t *o, char *name)
{
    /* the preset as written: magic 4, version 1, then the continuous parameters (16 bits) cpFreqA .. cpFilVelocity
     * (25), the stepped spASaw .. spLFOShape (10), one legacy byte, spLFOTargets .. spChromaticPitch (12); v2: 5 more
     * continuous, 2 stepped, 6 voice pattern bytes; v7: 12 tunings; v8: PWM bug, spread, external, env routing, assign,
     * LFO sync, the name (16) */
    enum { FreqA, VolA, APW, FreqB, VolB, BPW, FreqBFine, Cutoff, Resonance, FilEnvAmt, FilRel, FilSus, FilDec, FilAtt,
           AmpRel, AmpSus, AmpDec, AmpAtt, PModFilEnv, PModOscB, LFOFreq, LFOAmt, Glide, AmpVel, FilVel };
    enum { ASaw, ATri, ASqr, BSaw, BTri, BSqr, Sync, PModFA, PModFil, LFOShape };
    enum { LFOTargets, TrackingShift, Unison = 6 };
    static const uint8_t WAVE[6] = {3, 1, 4, 0, 4, 2};  /* GliGli's pulse tri rand sine noise saw -> SQR TRI S&H SIN S&H SAW */
    uint32_t cp[25], i, ver = buf[4], sp1 = 5 + 50, sp2 = sp1 + 11, v2 = sp2 + 12, v8;
    int32_t fb, fbi, va, vb, depth, tg, er = 0;
    for (i = 0; i < 25u; i++)
        cp[i] = p6_rd16(buf, 5u + 2u * i);
    fb = (int32_t)(cp[FreqB] >> 2) + ((int32_t)(cp[FreqBFine] >> 7) - 256);   /* B in 1/256 semitone */
    fbi = fb >> 8;
    va = (int32_t)cp[VolA];
    vb = (int32_t)cp[VolB];
    o->e[P6_A_WAV] = (int8_t)(buf[sp1 + ASaw] | buf[sp1 + ATri] << 1 | buf[sp1 + ASqr] << 2);
    o->e[P6_A_FRQ] = (int8_t)p6_clamp((int32_t)(cp[FreqA] + 512u) >> 10, 0, 63);
    o->e[P6_B_WAV] = (int8_t)(buf[sp1 + BSaw] | buf[sp1 + BTri] << 1 | buf[sp1 + BSqr] << 2);
    o->e[P6_B_FRQ] = (int8_t)p6_clamp(fbi, 0, 63);
    o->e[P6_CUT] = (int8_t)P6_CUT8[cp[Cutoff] >> 8];
    o->e[P6_RES] = (int8_t)p6_clamp((int32_t)(cp[Resonance] >> 10) * 2, 0, 127);
    o->e[P6_MIX] = (int8_t)(va + vb ? p6_clamp(127 * vb / (va + vb), 0, 127) : 64);
    o->e[P6_FENV] = (int8_t)p6_clamp(((int32_t)cp[FilEnvAmt] - 32768) * 137 / (2048 * 15), 0, 127);
    if (ver >= 8u) {
        v8 = v2 + 10u + 2u + 6u + 24u;
        er = buf[v8 + 5];
        for (i = 0; i < 15u; i++)
            name[i] = (char)(buf[v8 + 8 + i] >= 32u && buf[v8 + 8 + i] < 127u ? buf[v8 + 8 + i] : (buf[v8 + 8 + i] ? '?' : 0));
        name[15] = 0;
    }
    o->env[0] = P6_ENV_CV[cp[AmpAtt] >> 8]; o->env[1] = P6_ENV_CV[cp[AmpDec] >> 8];
    o->env[2] = (uint8_t)(cp[AmpSus] * 127u / 65535u); o->env[3] = P6_ENV_CV[cp[AmpRel] >> 8];
    o->x.fenv[0] = P6_ENV_CV[cp[FilAtt] >> 8]; o->x.fenv[1] = P6_ENV_CV[cp[FilDec] >> 8];
    o->x.fenv[2] = (uint8_t)(cp[FilSus] * 127u / 65535u); o->x.fenv[3] = P6_ENV_CV[cp[FilRel] >> 8];
    if (er == 2) {                                     /* the amplitude follows the filter envelope */
        for (i = 0; i < 4u; i++)
            o->env[i] = o->x.fenv[i];
    } else if (er == 3) {                              /* gate */
        o->env[0] = o->env[1] = o->env[3] = 0;
        o->env[2] = 127;
    }
    o->x.pw[0] = (uint8_t)(cp[APW] >> 9); o->x.pw[1] = (uint8_t)(cp[BPW] >> 9);
    o->x.fine = (uint8_t)p6_clamp((fb - (fbi << 8)) * 127 / 256, 0, 127);
    o->x.sync = buf[sp1 + Sync];
    o->x.pm[0] = (uint8_t)p6_clamp(((int32_t)cp[PModFilEnv] - 32768) * 127 / (2048 * 15), 0, 127);
    o->x.pm[1] = (uint8_t)(cp[PModOscB] >> 9);
    o->x.pm[2] = (uint8_t)(buf[sp1 + PModFA] | buf[sp1 + PModFil] << 1);
    o->x.kbd = (uint8_t)(buf[sp2 + TrackingShift] > 2u ? 2u : buf[sp2 + TrackingShift]);
    tg = buf[sp2 + LFOTargets];
    depth = (int32_t)((cp[LFOAmt] >> 8) * (cp[LFOAmt] >> 8) * 63u / 65025u);   /* (amt)^2, as make_bank.py */
    o->x.lfo[0] = P6_GLFO[cp[LFOFreq] >> 8];
    o->x.lfo[1] = WAVE[buf[sp1 + LFOShape] < 6u ? buf[sp1 + LFOShape] : 1u];
    o->x.lfod[0] = (int8_t)(tg & 1 ? 63 : 0); o->x.lfod[1] = (int8_t)(tg & 8 ? 63 : 0);
    o->x.lfod[2] = (int8_t)(tg & 2 ? 63 : 0);
    o->x.lfoamp = (uint8_t)(tg & 4 ? 127 : 0);
    o->x.wheel = (uint8_t)p6_clamp(64 * (63 - depth) / 63, 0, 63);
    o->x.glide = (uint8_t)(cp[Glide] > 0xC000u ? p6_clamp((int32_t)((cp[Glide] - 0xC000u) >> 10) * 6, 0, 127) : 0);
    o->x.unison = buf[sp2 + Unison] ? 1u : 0u;
    o->x.vel = (uint8_t)(cp[FilVel] * 40u / 65535u);
    o->x.detune = ver >= 2u ? (uint8_t)(p6_rd16(buf, v2 + 6u) >> 9) : 12u;   /* cpUnisonDetune (the 4th of v2's five) */
}

/* a dump (the bytes between F0 and F7) decoded into m (its name too); 0 = not a P600 program */
static int p6_decode(const uint8_t *f, uint32_t n, p6imp_t *m)
{
    static uint8_t g[160];
    uint32_t k, i;
    for (i = 0; i < sizeof m->name; i++)
        m->name[i] = 0;
    if (n == 35u && f[0] == 0x01u && f[1] == 0x02u && f[2] < 100u) {   /* Sequential's (SCI) program dump */
        p6_from_sci(f, m);
        m->name[0] = 'P'; m->name[1] = '6'; m->name[2] = '0'; m->name[3] = '0'; m->name[4] = ' ';
        m->name[5] = (char)('0' + f[2] / 10u); m->name[6] = (char)('0' + f[2] % 10u);
        return 1;
    }
    if (n > 9u && f[0] == 0x00u && f[1] == 0x61u && f[2] == 0x16u && f[3] == 0x01u) {   /* GliGli's */
        for (i = 0; i < sizeof g; i++)
            g[i] = 0;
        for (i = 4, k = 0; i < n && k + 4u <= sizeof g; i += 5u, k += 4u) {   /* 5 seven-bit bytes -> 4 */
            uint32_t j, hb = i + 4u < n ? f[i + 4u] : 0u;
            for (j = 0; j < 4u && i + j < n; j++)
                g[k + j] = (uint8_t)(f[i + j] | ((hb >> j) & 1u) << 7);
        }
        if ((g[1] | g[2] << 8 | (uint32_t)g[3] << 16) != 0x6116A5u)   /* STORAGE_MAGIC's low bytes */
            return 0;
        p6_from_gligli(g + 1, m, m->name);
        if (!m->name[0]) {
            m->name[0] = 'G'; m->name[1] = 'L'; m->name[2] = ' ';
            m->name[3] = (char)('0' + g[0] % 100u / 10u); m->name[4] = (char)('0' + g[0] % 10u);
        }
        return 1;
    }
    return 0;
}

static void p6_changed(void)
{
    p600_apply();
    p6_dirty = 1;
    p6_dirty_ms = fm1_ms;
}

/* forget every import: the 200 programs back, the free places empty (MENU > RESET SOUNDS, the send page); 1 = there
 * were some */
static int p600_reset(void)
{
    uint32_t i, had = 0;
    for (i = 0; i < P6_NIMP; i++) {
        had |= p6_imp[i].used;
        p6_imp[i].used = 0;
    }
    p6_changed();
    return (int)had;
}

/* p600_sysex's answers: P6SX_* | the place (EXPORT: editor.c sends p600_export's frame; LIST: p600_list's) */
enum { P6SX_KEPT = 0x100, P6SX_FULL = 0x200, P6SX_RESET = 0x300, P6SX_CLEARED = 0x400, P6SX_EXPORT = 0x500,
       P6SX_LIST = 0x600 };

/* m into place dest (0..254): its own import entry (a new one, or the one already there); the name as the fixed ones
 * show theirs, the place first. P6SX_KEPT | dest, or P6SX_FULL */
static uint32_t p6_put(uint32_t dest, p6imp_t *mm)
{
    static p6imp_t m;
    int32_t at;
    uint32_t i;
    m = *mm;
    at = p6_find(dest);
    for (i = 0; at < 0 && i < P6_NIMP; i++)
        if (!p6_imp[i].used)
            at = (int32_t)i;
    if (at < 0)
        return P6SX_FULL;                              /* P6_NIMP imports already */
    {   /* the place (1..255), then the program's name, as the fixed ones show theirs */
        char nm[16];
        uint32_t k = 0, pl = dest + 1u;
        if (pl >= 100u) nm[k++] = (char)('0' + pl / 100u);
        if (pl >= 10u) nm[k++] = (char)('0' + pl / 10u % 10u);
        nm[k++] = (char)('0' + pl % 10u);
        nm[k++] = ' ';
        for (i = 0; k < 15u && m.name[i]; i++)
            nm[k++] = m.name[i];
        nm[k] = 0;
        for (i = 0; i < 16u; i++)
            m.name[i] = i <= k ? nm[i] : 0;
    }
    m.dest = (uint8_t)dest;
    m.used = 1;
    p6_imp[at] = m;
    p6_changed();
    return P6SX_KEPT | dest;
}

/* a SysEx (the bytes between F0 and F7) for the P600? 0 = not one, else P6SX_* | the place */
static uint32_t p600_sysex(const uint8_t *f, uint32_t n)
{
    static p6imp_t m;
    int32_t at;
    uint32_t dest;
    if (n >= 4u && f[0] == 0x7Du && f[1] == 0x47u && f[2] == 0x36u) {   /* Guru 600's own frames */
        if (f[3] == 2u) {
            p600_reset();
            return P6SX_RESET;
        }
        if (f[3] == 5u)                                /* Guru-600: which places hold a kept sound */
            return P6SX_LIST;
        if (n < 6u || f[4] + (f[5] << 7) > 254u)
            return 0;
        dest = (uint32_t)f[4] + ((uint32_t)f[5] << 7);
        if (f[3] == 4u)                                /* Guru-600: send the place's sound back (p600_export) */
            return P6SX_EXPORT | dest;
        if (f[3] == 3u) {                              /* forget the one at dest */
            at = p6_find(dest);
            if (at >= 0)
                p6_imp[at].used = 0;
            p6_changed();
            return P6SX_CLEARED | dest;
        }
        if (f[3] != 1u || !p6_decode(f + 6, n - 6u, &m))
            return 0;
    } else {                                           /* a plain dump (no place named): the first place from 201
                                                        * that holds no import yet (Guru-600: 201..255 are built-in
                                                        * sounds too now; the send page always names a place) */
        if (!p6_decode(f, n, &m))
            return 0;
        for (dest = 200u; dest < 255u && p6_find(dest) >= 0; dest++)
            ;
        if (dest >= 255u)
            return P6SX_FULL;
    }
    return p6_put(dest, &m);
}

/* Guru-600: the sound in place dest (0..254) as an import entry: the kept one, else the fixed program (empty: the
 * empty place's) */
static void p6_of_place(uint32_t dest, p6imp_t *o)
{
    int32_t at = p6_find(dest);
    uint32_t k;
    if (at >= 0) {
        *o = p6_imp[at];
        return;
    }
    memset(o, 0, sizeof *o);
    for (k = 0; k < 8u; k++)
        o->e[k] = P600_PRESETS[dest < P600_NFIX ? dest : 0].e[k];
    for (k = 0; k < 4u; k++)
        o->env[k] = P600_PRESETS[dest < P600_NFIX ? dest : 0].env[k];
    o->x = dest < P600_NFIX ? P600_EXT[dest] : P6_EMPTY_EXT;
}

/* Guru-600: a track's P600 sound as an import entry (p600_preset backwards; VINTAGE and the sends are the track's) */
static void p6_from_track(const track_t *t, p6imp_t *o)
{
    const int16_t *p = t->p;
    uint32_t k;
    memset(o, 0, sizeof *o);
    for (k = 0; k < 8u; k++)
        o->e[k] = (int8_t)p[P_E0 + k];
    o->env[0] = (uint8_t)p[P_ATK]; o->env[1] = (uint8_t)p[P_DEC]; o->env[2] = (uint8_t)p[P_SUS]; o->env[3] = (uint8_t)p[P_REL];
    o->x.fenv[0] = (uint8_t)p[P6_FATK]; o->x.fenv[1] = (uint8_t)p[P6_FDEC];
    o->x.fenv[2] = (uint8_t)p[P6_FSUS]; o->x.fenv[3] = (uint8_t)p[P6_FREL];
    o->x.pw[0] = (uint8_t)p[P6_APW]; o->x.pw[1] = (uint8_t)p[P6_BPW];
    o->x.fine = (uint8_t)p[P6_BFIN]; o->x.sync = (uint8_t)p[P6_SYNC];
    o->x.pm[0] = (uint8_t)p[P6_PMENV]; o->x.pm[1] = (uint8_t)p[P6_PMB]; o->x.pm[2] = (uint8_t)p[P6_PMDST];
    o->x.kbd = (uint8_t)p[P6_KBD];
    o->x.lfo[0] = (uint8_t)p[P_LRATE]; o->x.lfo[1] = (uint8_t)p[P_LWAVE];
    o->x.lfod[0] = (int8_t)p[P_LD_PIT]; o->x.lfod[1] = (int8_t)p[P_LD_SHP]; o->x.lfod[2] = (int8_t)p[P_LD_FLT];
    o->x.lfoamp = (uint8_t)p[P_LD_AMP];
    o->x.vel = (uint8_t)p[P_M3AMT];
    o->x.wheel = (uint8_t)p[P_M4AMT];
    o->x.glide = (uint8_t)p[P_GLIDE];
    o->x.unison = (uint8_t)(p[P_VOICE] == V_UNISON);
    o->x.detune = (uint8_t)p[P_DETUNE];
}

/* a place's name without its number ("12 BRASS I" -> "BRASS I") into nm[16] */
static void p6_bare_name(uint32_t dest, char *nm)
{
    const char *s = dest < 255u && p6_ram[dest].name ? p6_ram[dest].name : "";
    uint32_t i = 0;
    while (*s >= '0' && *s <= '9')
        s++;
    while (*s == ' ')
        s++;
    for (; i < 15u && s[i]; i++)
        nm[i] = s[i];
    nm[i] = 0;
}

/* Guru-600 (the editor's RENAME, 10/11): a kept place's name (letters, digits, signs; 11 at most: the place number goes
 * first). 0 renamed, 1 memory full, 3 the place holds a factory sound (save it first) */
static uint32_t p600_rename(uint32_t dest, const uint8_t *s, uint32_t n)
{
    static p6imp_t m;
    int32_t at = p6_find(dest);
    uint32_t i;
    if (at < 0)
        return 3u;
    m = p6_imp[at];
    for (i = 0; i < 16u; i++)
        m.name[i] = i < n && i < 11u ? (char)(s[i] >= 0x20u && s[i] < 0x7Fu ? s[i] : '?') : 0;
    return (p6_put(dest, &m) & 0xF00u) == P6SX_KEPT ? 0u : 1u;
}

/* Guru-600 (SAVE > PLACE): the selected track's sound into place dest, with the name of the sound it came from (its
 * own place's name, not the replaced one's). P6SX_KEPT | dest, P6SX_FULL (no import entry left) */
static uint32_t p600_store_track(const track_t *t, uint32_t dest)
{
    static p6imp_t m;
    uint32_t src = t->preset;
    p6_from_track(t, &m);
    p6_bare_name(src < 255u ? src : dest, m.name);
    if (!m.name[0] || str_eq(m.name, "EMPTY"))
        str_cpy(m.name, "MY SOUND", 16);
    return p6_put(dest, &m);
}

/* Guru-600 (SAVE > PLACE ORIG): the place's own sound back (its kept one forgotten); 1 = there was one */
static int p600_forget(uint32_t dest)
{
    int32_t at = p6_find(dest);
    if (at < 0)
        return 0;
    p6_imp[at].used = 0;
    p6_changed();
    return 1;
}

/* Guru-600 export: Sequential's program dump, the Z80's 16 bytes (p6_from_sci backwards), as 01 02 nn and 32
 * nibbles into o[35]; the nearest value where the Guru-600 has more steps than the original */
static void p6_put_bits(uint8_t *b, uint32_t *pos, uint32_t w, uint32_t v)
{
    uint32_t i;
    for (i = 0; i < w; i++, (*pos)++)
        if ((v >> i) & 1u)
            b[*pos >> 3] |= (uint8_t)(1u << (*pos & 7u));
}
static uint32_t p6_near(const uint8_t *tab, uint32_t n, int32_t v)   /* the index of tab's value nearest v */
{
    uint32_t i, best = 0;
    int32_t bd = 1 << 30;
    for (i = 0; i < n; i++) {
        int32_t d = (int32_t)tab[i] - v;
        if (d < 0) d = -d;
        if (d < bd) { bd = d; best = i; }
    }
    return best;
}
static void p6_to_sci(const p6imp_t *m, uint32_t prog, uint8_t *o)
{
    uint8_t b[16];
    uint32_t pos = 0, k, wa = (uint32_t)m->e[P6_A_WAV] & 7u, wb = (uint32_t)m->e[P6_B_WAV] & 7u, la, depth;
    const p600_ext_t *x = &m->x;
    memset(b, 0, sizeof b);
    {   /* the LFO INITIAL AMOUNT whose wheel share (p6_from_sci) is nearest the sound's */
        int32_t bd = 1 << 30, d, w;
        uint32_t i;
        for (i = 0, la = 0; i < 32u; i++) {
            depth = i * i * 63u / 961u;
            w = p6_clamp(64 * (63 - (int32_t)depth) / 63, 0, 63);
            d = w - (int32_t)x->wheel;
            if (d < 0) d = -d;
            if (d < bd) { bd = d; la = i; }
        }
    }
    p6_put_bits(b, &pos, 7, x->pw[0]);
    p6_put_bits(b, &pos, 4, (uint32_t)p6_clamp(((int32_t)x->pm[0] * 15 + 63) / 127, 0, 15));
    p6_put_bits(b, &pos, 4, p6_near(P6_Z80_LFO, 16, x->lfo[0]));
    p6_put_bits(b, &pos, 7, x->pm[1]);
    p6_put_bits(b, &pos, 5, la);
    p6_put_bits(b, &pos, 6, (uint32_t)p6_clamp(m->e[P6_B_FRQ], 0, 63));
    p6_put_bits(b, &pos, 6, (uint32_t)p6_clamp(m->e[P6_A_FRQ], 0, 63));
    p6_put_bits(b, &pos, 7, x->fine);
    p6_put_bits(b, &pos, 6, (uint32_t)p6_clamp(m->e[P6_MIX] / 2, 0, 63));
    p6_put_bits(b, &pos, 7, p6_near(P6_CUT8, 128, m->e[P6_CUT]));
    p6_put_bits(b, &pos, 6, (uint32_t)p6_clamp(m->e[P6_RES] / 2, 0, 63));
    p6_put_bits(b, &pos, 4, (uint32_t)p6_clamp((m->e[P6_FENV] * 15 + 68) / 137, 0, 15));
    p6_put_bits(b, &pos, 4, p6_near(P6_Z80_ENV, 16, x->fenv[3]));
    p6_put_bits(b, &pos, 4, (uint32_t)p6_clamp(((int32_t)x->fenv[2] * 15 + 63) / 127, 0, 15));
    p6_put_bits(b, &pos, 4, p6_near(P6_Z80_ENV, 16, x->fenv[1]));
    p6_put_bits(b, &pos, 4, p6_near(P6_Z80_ENV, 16, x->fenv[0]));
    p6_put_bits(b, &pos, 4, p6_near(P6_Z80_ENV, 16, m->env[3]));
    p6_put_bits(b, &pos, 4, (uint32_t)p6_clamp(((int32_t)m->env[2] * 15 + 63) / 127, 0, 15));
    p6_put_bits(b, &pos, 4, p6_near(P6_Z80_ENV, 16, m->env[1]));
    p6_put_bits(b, &pos, 4, p6_near(P6_Z80_ENV, 16, m->env[0]));
    p6_put_bits(b, &pos, 4, (uint32_t)p6_clamp((x->glide + 3) / 6, 0, 15));
    p6_put_bits(b, &pos, 7, x->pw[1]);
    p6_put_bits(b, &pos, 1, (wa >> 2) & 1u); p6_put_bits(b, &pos, 1, (wb >> 2) & 1u);
    p6_put_bits(b, &pos, 1, x->kbd == 2u); p6_put_bits(b, &pos, 1, x->kbd == 1u);
    p6_put_bits(b, &pos, 1, x->lfo[1] == 1u); p6_put_bits(b, &pos, 1, x->lfod[0] != 0);
    p6_put_bits(b, &pos, 1, x->lfod[1] != 0); p6_put_bits(b, &pos, 1, x->lfod[2] != 0);
    p6_put_bits(b, &pos, 1, wa & 1u); p6_put_bits(b, &pos, 1, (wa >> 1) & 1u);
    p6_put_bits(b, &pos, 1, x->sync != 0); p6_put_bits(b, &pos, 1, wb & 1u);
    p6_put_bits(b, &pos, 1, (wb >> 1) & 1u); p6_put_bits(b, &pos, 1, x->pm[2] & 1u);
    p6_put_bits(b, &pos, 1, (x->pm[2] >> 1) & 1u); p6_put_bits(b, &pos, 1, x->unison != 0);
    o[0] = 0x01; o[1] = 0x02; o[2] = (uint8_t)(prog % 100u);
    for (k = 0; k < 16u; k++) {
        o[3 + 2 * k] = b[k] & 15u;
        o[4 + 2 * k] = b[k] >> 4;
    }
}

/* Guru-600: the answer to "send place dest": F0 7D 47 36 04 dest dest2, the name (16 bytes, 7 bit), the program dump
 * (35 bytes: 01 02 nn + 32 nibbles), F7 into o (60 bytes); its length */
static uint32_t p600_export(uint32_t dest, uint8_t *o)
{
    static p6imp_t m;
    uint32_t k, n = 0;
    p6_of_place(dest, &m);
    o[n++] = 0xF0; o[n++] = 0x7D; o[n++] = 0x47; o[n++] = 0x36; o[n++] = 4;
    o[n++] = (uint8_t)(dest & 0x7Fu); o[n++] = (uint8_t)(dest >> 7);
    for (k = 0; k < 16u; k++)
        o[n++] = (uint8_t)((dest < 255u && p6_ram[dest].name && k < str_len(p6_ram[dest].name)) ?
                           p6_ram[dest].name[k] & 0x7F : 0);
    p6_to_sci(&m, dest, o + n);
    if (dest < 100u && p6_find(dest) < 0)              /* an unmodified factory program: Sequential's own bytes */
        for (k = 0; k < 16u; k++) {
            o[n + 3u + 2u * k] = P6_SCI_FACT[dest][k] & 15u;
            o[n + 4u + 2u * k] = P6_SCI_FACT[dest][k] >> 4;
        }
    n += 35u;
    o[n++] = 0xF7;
    return n;
}

/* Guru-600: the answer to "which places hold a kept sound": F0 7D 47 36 05 count, then each place (2 bytes), F7 */
static uint32_t p600_list(uint8_t *o)
{
    uint32_t i, n = 6, c = 0;
    o[0] = 0xF0; o[1] = 0x7D; o[2] = 0x47; o[3] = 0x36; o[4] = 5;
    for (i = 0; i < P6_NIMP; i++)
        if (p6_imp[i].used) {
            o[n++] = (uint8_t)(p6_imp[i].dest & 0x7Fu);
            o[n++] = (uint8_t)(p6_imp[i].dest >> 7);
            c++;
        }
    o[5] = (uint8_t)c;
    o[n++] = 0xF7;
    return n;
}

/* the rest of a program (what preset_t has no room for), after ui.c apply_preset_to set the common part */
static void p600_preset(int16_t *p, uint32_t pi)      /* (Guru-600: an array, a track's or MORPH's B) */
{
    int32_t at = p6_find(pi);                          /* an import in that place: its own (the common part came
                                                        * from p6_ram already) */
    const p600_ext_t *x = at >= 0 ? &p6_imp[at].x : pi < P600_NFIX ? &P600_EXT[pi] : &P6_EMPTY_EXT;
    p[P6_FATK] = x->fenv[0];
    p[P6_FDEC] = x->fenv[1];
    p[P6_FSUS] = x->fenv[2];
    p[P6_FREL] = x->fenv[3];
    p[P6_APW] = x->pw[0];
    p[P6_BPW] = x->pw[1];
    p[P6_BFIN] = x->fine;
    p[P6_SYNC] = x->sync;
    p[P6_PMENV] = x->pm[0];
    p[P6_PMB] = x->pm[1];
    p[P6_PMDST] = x->pm[2];
    p[P6_KBD] = x->kbd;
    p[P6_VINT] = 24;                                  /* a little: the original's six voices never quite agree */
    p[P_LRATE] = x->lfo[0];
    p[P_LWAVE] = x->lfo[1];
    p[P_LD_PIT] = x->lfod[0];
    p[P_LD_SHP] = x->lfod[1];
    p[P_LD_FLT] = x->lfod[2];
    p[P_LD_AMP] = x->lfoamp;                          /* (GliGli's VCA target; the original has none) */
    p[P_M3AMT] = x->vel;                              /* EXTRAS VEL > FLT (ui.c sets its slot) */
    p[P_M4AMT] = (int16_t)x->wheel;                   /* EXTRAS WHEEL: the share of the LFO the mod wheel opens (the
                                                        * original's INITIAL AMOUNT + MOD wheel: ui.c, MODW -> DEPTH) */
    p[P_GLIDE] = x->glide;
    if (x->unison) {
        p[P_VOICE] = V_UNISON;
        p[P_DETUNE] = x->detune;                      /* the original stacks its voices, only its drift apart (12) */
    }
    p[P_ED_FLT] = 0;                                  /* the filter has its own envelope */
}

static engine_t ENG_P600 = {                         /* (not const: IMPORT grows npresets) */
    .name = "P600",
    .page_title = {"OSC", "FILTER"},
    .edit = {
        {"A WAV", F_ENUM, 0, 7, 1, N_P6_WAVE, 0},
        {"A FRQ", F_INT, 0, 63, 24, 0, "st"},
        {"B WAV", F_ENUM, 0, 7, 1, N_P6_WAVE, 0},
        {"B FRQ", F_INT, 0, 63, 24, 0, "st"},
        {"CUT", F_CUTOFF, 0, 127, 90, 0, 0},
        {"RES", F_PCT, 0, 127, 0, 0, 0},
        {"MIX", F_PCT, 0, 127, 64, 0, 0},
        {"FENV", F_PCT, 0, 127, 40, 0, 0},
    },
    .presets = P600_PRESETS,
    .npresets = P600_NFIX,
    .note_on = p600_note_on,
    .render = p600_render,
    .knob = {P_E0 + P6_CUT, P_E0 + P6_RES, P_E0 + P6_FENV, P_E0 + P6_MIX},
    .poly = 6,                   /* the original's six voices */
    .keep = 0xD3,                /* the ladder (s[0] s[1] s[6] s[7]) and the filter envelope's level (s[4]) */
};
