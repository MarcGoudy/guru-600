/* Captures de toutes les pages (moteur P600, accord tenu sur 250 CHIME PAD) : vérifie quelle animation va où.
 *   cc -O2 -w -I../Felucca/build/gen -I../Felucca/firmware/src -I../Felucca/web/emu -o build/all_pages_shot tests/all_pages_shot.c -lm
 *   build/all_pages_shot OUTDIR */
#include "felucca_web.c"

static const char *out;
static void run(double ms)
{
    uint32_t n = (uint32_t)(ms * 44.1 + 0.5), k;
    for (k = 0; k < n; k += 128u)
        web_render(n - k < 128u ? n - k : 128u);
}
static void shot(const char *name)
{
    char path[512];
    FILE *f;
    uint32_t i;
    snprintf(path, sizeof path, "%s/%s.ppm", out, name);
    f = fopen(path, "wb");
    fprintf(f, "P6\n240 240\n255\n");
    for (i = 0; i < 240u * 240u; i++) {
        uint16_t v = web_fb[i];
        v = (uint16_t)((v >> 8) | (v << 8));
        fputc(((v >> 11) & 31) * 255 / 31, f);
        fputc(((v >> 5) & 63) * 255 / 63, f);
        fputc((v & 31) * 255 / 31, f);
    }
    fclose(f);
}
int main(int argc, char **argv)
{
    uint32_t k, q;
    out = argv[1];
    web_nor_erase();
    web_boot();
    run(7000);
    set_engine_of(&trk[0], ENGI_P600);
    apply_preset_to(&trk[0], 249);
    run(100);
    for (q = 0; q < 4u; q++)
        trk_note_on(&trk[0], (uint8_t[4]){48, 55, 60, 67}[q], 100);
    ui.home = 1; ui.force = 1; run(1500); shot("00_HOME");
    if (argc > 2) {                                    /* (the MIXER, then FILTER: a jump each) */
        static const char *const SEQ[4] = {"FILTER", "MIXER", "MIXER", "FILTER"};
        uint32_t j;
        for (j = 0; j < 4u; j++) {
            char n[32];
            for (k = 0; k < NPAGES; k++)
                if (str_eq(PAGES[k].title, SEQ[j]) && PAGES[k].eng == ENGI_P600 + 1u)
                    break;
            ui.home = 0; ui.page = (uint8_t)k; ui.force = 1;
            run(j == 2u ? 4000 : 1500);
            snprintf(n, sizeof n, "seq%u_%s", j, SEQ[j]);
            shot(n);
        }
        return 0;
    }
    for (k = 0; k < NPAGES; k++) {
        char n[64], *c;
        if (PAGES[k].eng && PAGES[k].eng != ENGI_P600 + 1u)
            continue;
        ui.home = 0;
        ui.page = (uint8_t)k;
        ui.force = 1;
        run(1500);
        snprintf(n, sizeof n, "%02u_%s%s", (unsigned)k + 1u, PAGES[k].title, PAGES[k].eng ? "_p600" : "");
        for (c = n; *c; c++)
            if (*c == ' ' || *c == '/') *c = '_';
        shot(n);
        printf("%s g3=%u\n", n, (unsigned)g3_kind());
    }
    return 0;
}
