/* L'import SysEx du P600 (eng_p600.c p600_sysex) contre les banques intégrées (make_bank.py) : chaque programme de la
 * banque d'usine (dump SCI) et de la collection v2022 (dump GliGli) importé doit donner les mêmes valeurs.
 *   build/p600_import_test FACTORY.syx GLIGLI.syx */
#include "felucca_web.c"

static int nmsg(const uint8_t *d, long n, long *s, long *e, long from)
{
    long i;
    for (i = from; i < n && d[i] != 0xF0; i++)
        ;
    if (i >= n) return 0;
    *s = i + 1;
    for (i = *s; i < n && d[i] != 0xF7; i++)
        ;
    *e = i;
    return 1;
}
static uint8_t *load(const char *p, long *n)
{
    FILE *f = fopen(p, "rb");
    uint8_t *d;
    fseek(f, 0, SEEK_END); *n = ftell(f); fseek(f, 0, SEEK_SET);
    d = malloc((size_t)*n); fread(d, 1, (size_t)*n, f); fclose(f);
    return d;
}
static int cmp(uint32_t base, uint32_t k, uint32_t dest)
{
    const preset_t *pr = &P600_PRESETS[base + k];
    const p600_ext_t *a = &P600_EXT[base + k];
    int32_t at = p6_find(dest);
    const p6imp_t *m;
    int bad = 0, i;
    if (at < 0) { printf("  pas importé"); return 1; }
    m = &p6_imp[at];
    for (i = 0; i < 8; i++) if (pr->e[i] != m->e[i]) { printf("  e%d %d/%d", i, pr->e[i], m->e[i]); bad++; }
    for (i = 0; i < 4; i++) if (pr->env[i] != m->env[i]) { printf("  env%d %d/%d", i, pr->env[i], m->env[i]); bad++; }
    if (memcmp(a, &m->x, sizeof *a)) {
        const uint8_t *x = (const uint8_t *)a, *y = (const uint8_t *)&m->x;
        for (i = 0; i < (int)sizeof *a; i++) if (x[i] != y[i]) { printf("  x[%d] %d/%d", i, x[i], y[i]); bad++; }
    }
    return bad;
}
static uint32_t wrap(uint32_t dest, const uint8_t *p, uint32_t n)   /* F0 7D 47 36 01 dest dest2 p F7 */
{
    static uint8_t f[700];
    f[0] = 0x7D; f[1] = 0x47; f[2] = 0x36; f[3] = 1; f[4] = dest & 127u; f[5] = (uint8_t)(dest >> 7);
    memcpy(f + 6, p, n);
    return p600_sysex(f, n + 6u);
}
int main(int argc, char **argv)
{
    long n1, n2, s, e, at = 0;
    uint8_t *d1 = load(argv[1], &n1), *d2 = load(argv[2], &n2);
    uint32_t k = 0, bad = 0, r;
    web_nor_erase();
    web_boot();
    p600_boot();
    p600_reset();
    while (nmsg(d1, n1, &s, &e, at) && k < 55u) {      /* into places 201.. (dest 200 + k) */
        r = wrap(200u + k, d1 + s, (uint32_t)(e - s));
        if (cmp(0, k, 200u + k)) { printf("  <- SCI %u\n", k); bad++; }
        at = e + 1; k++;
    }
    printf("SCI : %u programmes, %u différents\n", k, bad);
    p600_reset();
    at = 0; k = 0; bad = 0;
    while (nmsg(d2, n2, &s, &e, at) && k < 55u) {
        r = wrap(200u + k, d2 + s, (uint32_t)(e - s));
        if (cmp(100, k, 200u + k)) { printf("  <- GliGli %u\n", k); bad++; }
        at = e + 1; k++;
    }
    printf("GliGli : %u programmes, %u différents ; PRESETS : %u ; nom 201 : %s\n", k, bad, ENG_P600.npresets,
           ENG_P600.presets[200].name);
    (void)r;
    return 0;
}
