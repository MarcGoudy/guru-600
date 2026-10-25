/* Guru-600 : enregistrer un son à sa place, rétablir l'original, exporter (aller-retour SCI), page SAVE > PLACE.
 *   cc -O2 -w -I../Felucca/build/gen -I../Felucca/firmware/src -I../Felucca/web/emu -o build/p600_place_test tests/p600_place_test.c -lm
 *   build/p600_place_test OUTDIR */
#include "felucca_web.c"
static void run(double ms)
{
    uint32_t n = (uint32_t)(ms * 44.1 + 0.5), k;
    for (k = 0; k < n; k += 128u)
        web_render(n - k < 128u ? n - k : 128u);
}
static void tap(uint32_t b, double after) { web_buttons(1u << b); run(70); web_buttons(0); run(after); }
static void shot(const char *dir, const char *name)
{
    char path[512];
    FILE *f;
    uint32_t i;
    snprintf(path, sizeof path, "%s/%s.ppm", dir, name);
    f = fopen(path, "wb");
    fprintf(f, "P6\n240 240\n255\n");
    for (i = 0; i < 240u * 240u; i++) {
        uint16_t v = web_fb[i];
        v = (uint16_t)((v >> 8) | (v << 8));
        fputc(((v >> 11) & 31) * 255 / 31, f); fputc(((v >> 5) & 63) * 255 / 63, f); fputc((v & 31) * 255 / 31, f);
    }
    fclose(f);
}
static int same(const p6imp_t *a, const p6imp_t *b, char *why)
{
    int k;
    for (k = 0; k < 8; k++) if (a->e[k] != b->e[k]) { sprintf(why, "e[%d] %d/%d", k, a->e[k], b->e[k]); return 0; }
    for (k = 0; k < 4; k++) if (a->env[k] != b->env[k]) { sprintf(why, "env[%d] %d/%d", k, a->env[k], b->env[k]); return 0; }
    if (memcmp(&a->x, &b->x, sizeof a->x)) {
        const uint8_t *p = (const uint8_t *)&a->x, *q = (const uint8_t *)&b->x;
        for (k = 0; k < (int)sizeof a->x; k++) if (p[k] != q[k]) { sprintf(why, "ext byte %d %d/%d", k, p[k], q[k]); break; }
        return 0;
    }
    return 1;
}
int main(int argc, char **argv)
{
    static p6imp_t a, b;
    uint8_t sci[35], o[64];
    char why[64];
    uint32_t i, ok = 0, n;
    web_nor_erase(); web_boot(); run(7000);
    /* 1. aller-retour : les 100 sons d'usine -> SCI -> relus */
    for (i = 0; i < 100u; i++) {
        p6_of_place(i, &a);
        p6_to_sci(&a, i, sci);
        memset(&b, 0, sizeof b);
        if (!p6_decode(sci, 35, &b)) { printf("place %u : SCI illisible\n", i + 1); continue; }
        if (same(&a, &b, why)) ok++; else printf("place %u differe : %s\n", i + 1, why);
    }
    printf("aller-retour SCI : %u / 100 identiques\n", ok);
    /* 2. enregistrer un son modifie a sa place */
    apply_preset_to(TSEL, 1);                                   /* 2 CL. BRASS */
    TSEL->p[P_E0 + P6_CUT] = 20;
    printf("store : %x\n", p600_store_track(TSEL, 1));
    apply_preset_to(TSEL, 0);
    apply_preset_to(TSEL, 1);
    printf("place 2 apres enregistrement : cutoff %d (20 attendu), nom %s\n", TSEL->p[P_E0 + P6_CUT], p6_ram[1].name);
    /* 3. export de la place 2 */
    { uint8_t f[8] = {0x7D, 0x47, 0x36, 4, 1, 0}; uint32_t s = p600_sysex(f, 6);
      printf("export : code %x ; trame %u octets\n", s, n = p600_export(s & 0xFFu, o)); }
    { uint8_t f[4] = {0x7D, 0x47, 0x36, 5}; uint32_t s = p600_sysex(f, 4), m = p600_list(o);
      printf("liste : code %x, %u place(s), %u octets\n", s, o[5], m); }
    /* 4. la page SAVE > PLACE */
    tap(B_SAVE, 600); tap(B_SAVE, 600);
    printf("page : %s\n", ui.home ? "HOME" : PAGES[ui.page].title);
    shot(argv[1], "place");
    /* 5. retour a l'original */
    printf("forget : %d\n", p600_forget(1));
    apply_preset_to(TSEL, 1);
    printf("place 2 apres ORIG : cutoff %d, nom %s\n", TSEL->p[P_E0 + P6_CUT], p6_ram[1].name);
    return 0;
}
