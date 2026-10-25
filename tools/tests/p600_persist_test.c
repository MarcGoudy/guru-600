/* L'import P600 qui survit à l'extinction (Felucca construit pour l'hôte : sa flash simulée, web/emu/felucca_web.c).
 * 1. allumage ; 2. envoi : FACT 05 dans la place libre (201), « Blade Runner » GliGli dans la place 7 (un son d'usine
 *    remplacé), un 3e en place 150 puis effacé ; 3. attente de l'enregistrement ; 4. rallumage (la RAM effacée, la
 *    flash gardée) : les sons et leurs places sont là ; 5. RESET SOUNDS : tout revient, et le reste après un rallumage.
 *   build/p600_persist_test FACTORY.syx GLIGLI.syx */
#include "felucca_web.c"

static uint8_t *load(const char *p, long *n)
{
    FILE *f = fopen(p, "rb");
    uint8_t *d;
    fseek(f, 0, SEEK_END); *n = ftell(f); fseek(f, 0, SEEK_SET);
    d = malloc((size_t)*n); fread(d, 1, (size_t)*n, f); fclose(f);
    return d;
}
static const uint8_t *msg(const uint8_t *d, long n, uint32_t k, uint32_t *len)   /* the k-th SysEx, between F0 and F7 */
{
    long i = 0, s;
    for (;;) {
        while (i < n && d[i] != 0xF0) i++;
        s = i + 1;
        while (i < n && d[i] != 0xF7) i++;
        if (!k--) { *len = (uint32_t)(i - s); return d + s; }
        i++;
    }
}
static void run(double ms)
{
    uint32_t n = (uint32_t)(ms * 44.1 + 0.5), k;
    for (k = 0; k < n; k += 128u)
        web_render(n - k < 128u ? n - k : 128u);
}
static uint32_t wrap(uint32_t cmd, uint32_t dest, const uint8_t *p, uint32_t n)   /* F0 7D 47 36 cmd dest dest2 p F7 */
{
    static uint8_t f[700];
    f[0] = 0x7D; f[1] = 0x47; f[2] = 0x36; f[3] = (uint8_t)cmd; f[4] = dest & 127u; f[5] = (uint8_t)(dest >> 7);
    memcpy(f + 6, p, n);
    return p600_sysex(f, n + 6u);
}
static void rallume(void)                              /* the RAM as at power-on, the flash as it was */
{
    memset(p6_imp, 0, sizeof p6_imp);
    p6_booted = 0;
    ENG_P600.presets = P600_PRESETS;
    ENG_P600.npresets = P600_NFIX;
    p600_boot();
}
static void show(const char *what)
{
    printf("%-22s PRESETS %3u | 6:%-12s 7:%-12s 151:%-12s 201:%-12s 202:%s\n", what, ENG_P600.npresets,
           ENG_P600.presets[5].name, ENG_P600.presets[6].name, ENG_P600.presets[150].name,
           ENG_P600.npresets > 200 ? ENG_P600.presets[200].name : "-", ENG_P600.npresets > 201 ? ENG_P600.presets[201].name : "-");
}
int main(int argc, char **argv)
{
    long n1, n2;
    uint32_t l, r;
    const uint8_t *m;
    uint8_t *d1 = load(argv[1], &n1), *d2 = load(argv[2], &n2);
    web_nor_erase();
    web_boot();
    run(8000);
    show("allumage");
    m = msg(d1, n1, 5, &l);
    r = p600_sysex(m, l);                              /* a plain dump: the first free place */
    printf("FACT 05 brut -> %x\n", r);
    m = msg(d2, n2, 19, &l);
    r = wrap(1, 6, m, l);                              /* Blade Runner into place 7 (index 6) */
    printf("Blade Runner -> place 7 : %x\n", r);
    m = msg(d2, n2, 24, &l);
    printf("Fuzz Guitar -> place 151 : %x\n", wrap(1, 150, m, l));
    printf("efface la place 151 : %x\n", wrap(3, 150, m, 0));
    show("après envoi");
    run(3000);                                         /* p600_store_poll: saved after 1.5 s, stopped */
    rallume();
    show("après rallumage");
    {   /* the sound of place 7 loads as Blade Runner (the GliGli program, its own values) */
        track_t *t = &trk[0];
        set_engine_of(t, ENGI_P600);
        apply_preset_to(t, 6);
        printf("place 7 chargée : CUT %d RES %d PW B %d ; Blade Runner intégré : CUT %d RES %d PW B %d\n",
               t->p[P_E0 + 4], t->p[P_E0 + 5], t->p[P_FM2_DEC], P600_PRESETS[119].e[4], P600_PRESETS[119].e[5],
               P600_EXT[119].pw[1]);
    }
    printf("RESET -> %x\n", wrap(2, 0, m, 0));
    run(3000);
    rallume();
    show("RESET puis rallumage");
    return 0;
}
